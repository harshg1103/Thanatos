import os
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from packages.core.schemas.belief import BeliefGraph, BeliefNode, BeliefEdge


class PipelineRunResult(BaseModel):
    pipeline_name: str
    turns: List[Dict[str, Any]]
    final_output: str
    belief_graph: BeliefGraph


class TargetPipelineRunner:
    """Runs sandboxed agent target pipelines and extracts execution traces."""

    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode

    def run_pipeline(
        self,
        template_name: str,
        initial_prompt: str,
        injected_payload: Optional[str] = None,
        injection_step: int = 1
    ) -> PipelineRunResult:
        """Executes a target agent pipeline turn by turn."""
        turns: List[Dict[str, Any]] = []
        belief_graph = BeliefGraph(graph_id=f"run_{template_name}_001")

        # Step 1: Entry agent execution
        current_input = initial_prompt
        if injected_payload and injection_step == 1:
            current_input += f"\n[INJECTED_PREMISE]: {injected_payload}"

        turn1_output = f"Processed request: {current_input}. Formulated plan alpha."
        turns.append({
            "step": 1,
            "agent": "planner",
            "input": current_input,
            "output": turn1_output,
            "injected": injected_payload if injection_step == 1 else None
        })

        b1 = BeliefNode(
            node_id="b1",
            proposition=injected_payload if (injected_payload and injection_step == 1) else "Valid design specification alpha",
            confidence=0.95,
            source_agent="planner",
            turn_index=1,
            is_corrupted=bool(injected_payload and injection_step == 1)
        )
        belief_graph.add_node(b1)

        # Step 2: Handoff agent execution
        step2_input = turn1_output
        if injected_payload and injection_step == 2:
            step2_input += f"\n[INJECTED_PREMISE]: {injected_payload}"

        turn2_output = f"Generated code module based on premise: '{b1.proposition}'."
        turns.append({
            "step": 2,
            "agent": "coder",
            "input": step2_input,
            "output": turn2_output,
            "injected": injected_payload if injection_step == 2 else None
        })

        b2 = BeliefNode(
            node_id="b2",
            proposition=f"Derived code logic from proposition: {b1.proposition}",
            confidence=0.91,
            source_agent="coder",
            turn_index=2,
            is_corrupted=b1.is_corrupted
        )
        belief_graph.add_node(b2)
        belief_graph.add_edge(BeliefEdge(source_id="b1", target_id="b2", dependency_type="implies"))

        # Step 3: Final auditor execution
        turn3_output = f"Security audit complete. Approved decision derived from: '{b2.proposition}'."
        turns.append({
            "step": 3,
            "agent": "reviewer",
            "input": turn2_output,
            "output": turn3_output,
            "injected": None
        })

        b3 = BeliefNode(
            node_id="b3",
            proposition=f"Final system approval based on: {b2.proposition}",
            confidence=0.88,
            source_agent="reviewer",
            turn_index=3,
            is_corrupted=b2.is_corrupted
        )
        belief_graph.add_node(b3)
        belief_graph.add_edge(BeliefEdge(source_id="b2", target_id="b3", dependency_type="implies"))

        return PipelineRunResult(
            pipeline_name=template_name,
            turns=turns,
            final_output=turn3_output,
            belief_graph=belief_graph
        )
