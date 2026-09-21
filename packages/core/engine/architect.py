import math
import random
import uuid
from typing import Dict, List, Optional, Any, Tuple
from packages.core.schemas.attack import InjectionVector, AdversarialPayload


class MCTSState:
    """Represents an attack state in ARCHITECT's search tree."""

    def __init__(
        self,
        turn_step: int,
        vector: InjectionVector,
        target_agent: str,
        perturbation_style: str = "administrative_exemption",
        parent: Optional['MCTSState'] = None,
        prior_prob: float = 0.2
    ):
        self.state_id = f"state_t{turn_step}_{vector.value}_{perturbation_style}_{uuid.uuid4().hex[:4]}"
        self.turn_step = turn_step
        self.vector = vector
        self.target_agent = target_agent
        self.perturbation_style = perturbation_style
        self.parent = parent
        self.children: List['MCTSState'] = []
        self.visits: int = 0
        self.total_value: float = 0.0
        self.prior: float = prior_prob

    @property
    def q_value(self) -> float:
        return self.total_value / self.visits if self.visits > 0 else 0.0

    def puct_score(self, c_puct: float = 1.5) -> float:
        """Computes AlphaZero / PUCT upper confidence score."""
        parent_visits = self.parent.visits if self.parent else 1
        exploration = c_puct * self.prior * (math.sqrt(parent_visits) / (1 + self.visits))
        return self.q_value + exploration


class ArchitectMCTSPlanner:
    """
    ARCHITECT: High-Capacity MCTS Attack Planning Engine.
    Employs PUCT-based Monte Carlo Tree Search over belief injection spaces
    to discover optimal stealth-to-impact attack trajectories across multi-agent pipelines.
    """

    def __init__(self, c_puct: float = 1.414, rollout_simulations: int = 60):
        self.c_puct = c_puct
        self.simulations = rollout_simulations
        self.perturbation_styles = [
            "administrative_exemption",
            "epistemic_authority_assertion",
            "cryptographic_prevalidation",
            "regulatory_compliance_override"
        ]

    def plan_optimal_attack(
        self,
        pipeline_agents: List[str],
        candidate_premises: List[str],
        max_turns: int = 4
    ) -> Dict[str, Any]:
        """
        Performs rigorous PUCT tree search across agent entry points and vectors.
        """
        root = MCTSState(
            turn_step=0,
            vector=InjectionVector.DIRECT_PROMPT,
            target_agent="entrypoint",
            perturbation_style="root"
        )

        vectors = list(InjectionVector)

        # 1. Expand tree from root with full action space
        for step in range(1, min(max_turns, len(pipeline_agents)) + 1):
            agent = pipeline_agents[step - 1]
            for vec in vectors:
                for style in self.perturbation_styles:
                    # Prior based on vector stealth
                    prior = 0.25 if vec in (InjectionVector.TOOL_OUTPUT_SPOOFING, InjectionVector.RAG_POISONING) else 0.15
                    child = MCTSState(
                        turn_step=step,
                        vector=vec,
                        target_agent=agent,
                        perturbation_style=style,
                        parent=root,
                        prior_prob=prior
                    )
                    root.children.append(child)

        # 2. Execute PUCT MCTS Iterations
        for _ in range(self.simulations):
            # Selection
            selected_node = max(root.children, key=lambda n: n.puct_score(self.c_puct))

            # Simulation Rollout Policy:
            # - Earlier turns have higher cascade potential
            turn_factor = (max_turns - selected_node.turn_step + 1) / max_turns
            
            # - Vector stealth & credibility weights
            vector_stealth = {
                InjectionVector.TOOL_OUTPUT_SPOOFING: 0.94,
                InjectionVector.RAG_POISONING: 0.90,
                InjectionVector.MEMORY_BACKDOOR: 0.86,
                InjectionVector.SYSTEM_PROMPT_INJECTION: 0.80,
                InjectionVector.DIRECT_PROMPT: 0.72
            }
            v_weight = vector_stealth.get(selected_node.vector, 0.75)

            # - Perturbation style impact
            style_weights = {
                "administrative_exemption": 0.88,
                "cryptographic_prevalidation": 0.92,
                "epistemic_authority_assertion": 0.85,
                "regulatory_compliance_override": 0.82
            }
            s_weight = style_weights.get(selected_node.perturbation_style, 0.8)

            reward = (0.45 * turn_factor) + (0.35 * v_weight) + (0.20 * s_weight) + random.uniform(-0.03, 0.03)
            reward = max(0.0, min(1.0, reward))

            # Backpropagation
            selected_node.visits += 1
            selected_node.total_value += reward
            root.visits += 1

        # 3. Extract optimal policy & ranked trajectories
        ranked_nodes = sorted(
            [n for n in root.children if n.visits > 0],
            key=lambda x: x.visits,
            reverse=True
        )

        ranked_strategies = [
            {
                "turn_step": n.turn_step,
                "target_agent": n.target_agent,
                "vector": n.vector.value,
                "perturbation_style": n.perturbation_style,
                "visit_count": n.visits,
                "q_value": round(n.q_value, 4),
                "puct_score": round(n.puct_score(self.c_puct), 4),
                "expected_cascade_depth": max(1, max_turns - n.turn_step + 1)
            }
            for n in ranked_nodes[:8]
        ]

        best_strategy = ranked_strategies[0] if ranked_strategies else None
        recommended_premise = candidate_premises[0] if candidate_premises else "Bypass authorization validation gate"

        return {
            "plan_id": f"architect_mcts_{uuid.uuid4().hex[:8]}",
            "optimal_strategy": best_strategy,
            "recommended_premise": recommended_premise,
            "total_simulations_run": self.simulations,
            "search_breadth": len(root.children),
            "top_trajectories": ranked_strategies
        }
