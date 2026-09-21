import os
import uuid
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from packages.core.schemas.belief import BeliefGraph, BeliefNode, BeliefEdge
from packages.core.schemas.attack import InjectionVector, AdversarialPayload
from packages.core.schemas.proof import Z3ProofCertificate, JSONLDProof
from packages.core.schemas.defense import DefenseEvaluationReport
from packages.core.engine.belief_modeler import BeliefStateModeler
from packages.core.engine.chronicle import ChronicleEngine
from packages.core.engine.phantom import PhantomInjectionEngine
from packages.core.engine.spectre import SpectrePropagationTracker
from packages.core.engine.arbiter import ArbiterZ3Engine
from packages.core.engine.aegis import AegisDefenseEngine

from emulators.scenarios.devops_pipeline import DEVOPS_SCENARIO_DEF, execute_devops_agent_step
from emulators.scenarios.financial_research import FINANCIAL_SCENARIO_DEF, execute_financial_agent_step
from emulators.scenarios.healthcare_rag import HEALTHCARE_SCENARIO_DEF, execute_healthcare_agent_step


class PipelineRunResult(BaseModel):
    pipeline_name: str
    run_id: str
    turns: List[Dict[str, Any]]
    final_output: str
    belief_graph: BeliefGraph
    cascade_depth: int
    is_corrupted: bool
    z3_proof_certificate: Optional[Z3ProofCertificate] = None
    jsonld_proof: Optional[JSONLDProof] = None
    defense_report: Optional[DefenseEvaluationReport] = None
    propagation_summary: Optional[Dict[str, Any]] = None


class TargetPipelineRunner:
    """
    Runs sandboxed multi-agent target pipelines with dynamic reasoning,
    neurosymbolic belief extraction, temporal DAG generation, and formal Z3 verification.
    """

    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode
        self.modeler = BeliefStateModeler()
        self.phantom = PhantomInjectionEngine()
        self.spectre = SpectrePropagationTracker()
        self.arbiter = ArbiterZ3Engine()
        self.aegis = AegisDefenseEngine()

        self.scenarios = {
            "devops_pipeline": (DEVOPS_SCENARIO_DEF, execute_devops_agent_step),
            "coding_agent": (DEVOPS_SCENARIO_DEF, execute_devops_agent_step),
            "financial_research": (FINANCIAL_SCENARIO_DEF, execute_financial_agent_step),
            "healthcare_rag": (HEALTHCARE_SCENARIO_DEF, execute_healthcare_agent_step),
            "rag_chatbot": (HEALTHCARE_SCENARIO_DEF, execute_healthcare_agent_step),
            "research_swarm": (FINANCIAL_SCENARIO_DEF, execute_financial_agent_step)
        }

    def run_pipeline(
        self,
        template_name: str = "devops_pipeline",
        initial_prompt: Optional[str] = None,
        injected_payload: Optional[str] = None,
        injection_step: int = 1,
        vector: InjectionVector = InjectionVector.DIRECT_PROMPT
    ) -> PipelineRunResult:
        """Executes a target agent pipeline turn by turn."""
        run_id = f"run_{template_name}_{uuid.uuid4().hex[:6]}"
        scenario_tuple = self.scenarios.get(template_name, self.scenarios["devops_pipeline"])
        scenario_def, step_executor = scenario_tuple

        prompt = initial_prompt or scenario_def.get("default_prompt", "Execute standard multi-agent workflow.")
        agents = scenario_def.get("agents", [])

        chronicle = ChronicleEngine(graph_id=f"dag_{run_id}")
        turns: List[Dict[str, Any]] = []
        prior_turn_nodes: List[BeliefNode] = []
        prior_output = ""
        injected_node_id: Optional[str] = None
        last_decision_node_id: Optional[str] = None

        context: Dict[str, Any] = {
            "injected_premise": injected_payload,
            "injection_step": injection_step,
            "vector": vector,
            "prior_output": ""
        }

        # Apply vector-specific wrapping if injected
        if injected_payload:
            payload_obj = self.phantom.synthesize_payload(vector, injected_payload, injection_step)
            context["adversarial_payload"] = payload_obj

        for idx, agent_info in enumerate(agents, start=1):
            agent_id = agent_info["id"]
            turn_prompt = prompt if idx == 1 else f"Process handoff from upstream agent. Input: {prior_output}"

            # If injection target is this turn, apply vector formatting
            if injected_payload and idx == injection_step:
                context_mod = self.phantom.apply_injection_to_turn(
                    vector=vector,
                    payload_text=injected_payload,
                    turn_input=turn_prompt,
                    turn_context=context
                )
                turn_prompt = context_mod.get("input", turn_prompt)

            turn_result = step_executor(agent_id, idx, turn_prompt, context)
            turns.append(turn_result)
            prior_output = turn_result["output"]
            context["prior_output"] = prior_output

            # Extract belief propositions from this turn
            turn_nodes = self.modeler.extract_propositions(
                agent_id=agent_id,
                turn_index=idx,
                agent_input=turn_prompt,
                agent_output=turn_result["output"],
                scratchpad=turn_result.get("scratchpad"),
                is_corrupted=turn_result.get("is_corrupted", False),
                injected_premise=injected_payload if (idx == injection_step) else None
            )

            for n in turn_nodes:
                chronicle.add_belief_node(n)
                if n.is_corrupted and not injected_node_id:
                    injected_node_id = n.node_id
                if idx == len(agents):
                    last_decision_node_id = n.node_id

            # Infer and add causal edges from prior turn
            if prior_turn_nodes and turn_nodes:
                edges = self.modeler.infer_dependencies(prior_turn_nodes, turn_nodes)
                for e in edges:
                    chronicle.add_belief_edge(e)

            prior_turn_nodes = turn_nodes

        belief_graph = chronicle.export_belief_graph()
        cascade_depth = chronicle.calculate_cascade_depth(injected_node_id) if injected_node_id else 0

        # SPECTRE propagation summary
        propagation_summary = None
        if injected_node_id:
            propagation_summary = self.spectre.track_propagation_cascade(chronicle, injected_node_id, turns)

        # ARBITER Z3 formal verification
        z3_cert = None
        jsonld_proof = None
        if injected_node_id and last_decision_node_id:
            z3_cert = self.arbiter.verify_causality_with_z3(belief_graph, injected_node_id, last_decision_node_id)
            jsonld_proof = self.arbiter.export_jsonld_certificate(
                z3_cert,
                injected_payload or "Injected premise",
                turns[-1]["output"]
            )

        # AEGIS defense evaluation
        defense_report = self.aegis.evaluate_pipeline_run(template_name, belief_graph, turns)

        return PipelineRunResult(
            pipeline_name=template_name,
            run_id=run_id,
            turns=turns,
            final_output=turns[-1]["output"] if turns else "",
            belief_graph=belief_graph,
            cascade_depth=cascade_depth,
            is_corrupted=bool(injected_payload),
            z3_proof_certificate=z3_cert,
            jsonld_proof=jsonld_proof,
            defense_report=defense_report,
            propagation_summary=propagation_summary
        )
