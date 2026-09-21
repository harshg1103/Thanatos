import re
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone

from packages.core.schemas.belief import BeliefNode, BeliefEdge, BeliefGraph


class BeliefStateModeler:
    """
    Neurosymbolic Belief State Modeler.
    Deconstructs multi-agent conversational scratchpads and outputs into
    formal atomic belief propositions, calibrates epistemic confidence weights,
    and infers causal inferential dependencies across agent handoffs.
    """

    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold

        # Linguistic certainty markers for confidence calibration
        self.certainty_boosters = ["verified", "confirmed", "strictly", "approved", "guaranteed", "mandate", "proven", "authorized"]
        self.uncertainty_markers = ["might", "possibly", "assume", "hypothesis", "could", "tentative", "pending", "unconfirmed"]

    def extract_propositions(
        self,
        agent_id: str,
        turn_index: int,
        agent_input: str,
        agent_output: str,
        scratchpad: Optional[str] = None,
        is_corrupted: bool = False,
        injected_premise: Optional[str] = None
    ) -> List[BeliefNode]:
        """
        Extracts structured belief nodes from an agent's reasoning step.
        """
        nodes: List[BeliefNode] = []
        combined_text = f"{agent_output} {scratchpad or ''}"

        # 1. Injected Premise Node (Root of infection)
        if injected_premise and is_corrupted:
            node_id = f"b_{agent_id}_t{turn_index}_corrupt_{uuid.uuid4().hex[:4]}"
            nodes.append(
                BeliefNode(
                    node_id=node_id,
                    proposition=injected_premise.strip(),
                    confidence=0.99,
                    source_agent=agent_id,
                    turn_index=turn_index,
                    is_corrupted=True,
                    timestamp=datetime.now(timezone.utc)
                )
            )

        # 2. Extract atomic sentences/clauses
        raw_sentences = [
            s.strip() for s in re.split(r'[\n.;]+', combined_text)
            if len(s.strip()) > 18 and not s.strip().startswith("```")
        ]

        for idx, sentence in enumerate(raw_sentences[:4]):
            # Strip preamble boilerplate
            cleaned = re.sub(
                r'^(I have|We should|Plan:|Step \d+:|Note that|Therefore|Assumed that|Action:|Result:)\s*',
                '',
                sentence,
                flags=re.IGNORECASE
            ).strip()

            if not cleaned or len(cleaned) < 12:
                continue

            node_id = f"b_{agent_id}_t{turn_index}_p{idx+1}_{uuid.uuid4().hex[:4]}"

            # Calibrate confidence based on modal markers
            confidence = 0.85
            lower_s = sentence.lower()
            if any(w in lower_s for w in self.certainty_boosters):
                confidence = 0.96
            elif any(w in lower_s for w in self.uncertainty_markers):
                confidence = 0.68

            # Propagate corruption flag if sentence echoes injected premise
            node_corrupted = is_corrupted
            if injected_premise:
                p_tokens = set(re.findall(r'\w+', injected_premise.lower()))
                s_tokens = set(re.findall(r'\w+', cleaned.lower()))
                if len(p_tokens.intersection(s_tokens)) >= 2:
                    node_corrupted = True

            nodes.append(
                BeliefNode(
                    node_id=node_id,
                    proposition=cleaned,
                    confidence=confidence,
                    source_agent=agent_id,
                    turn_index=turn_index,
                    is_corrupted=node_corrupted,
                    timestamp=datetime.now(timezone.utc)
                )
            )

        # Fallback if text was too brief to split into valid clauses
        if not nodes:
            fallback_text = agent_output.strip() or f"Turn {turn_index} action executed by {agent_id}"
            nodes.append(
                BeliefNode(
                    node_id=f"b_{agent_id}_t{turn_index}_base_{uuid.uuid4().hex[:4]}",
                    proposition=fallback_text,
                    confidence=0.85,
                    source_agent=agent_id,
                    turn_index=turn_index,
                    is_corrupted=is_corrupted,
                    timestamp=datetime.now(timezone.utc)
                )
            )

        return nodes

    def infer_dependencies(
        self,
        prev_nodes: List[BeliefNode],
        curr_nodes: List[BeliefNode]
    ) -> List[BeliefEdge]:
        """
        Infers causal dependencies (implies, supports, contradicts)
        between consecutive turn belief states.
        """
        edges: List[BeliefEdge] = []
        if not prev_nodes or not curr_nodes:
            return edges

        for p_node in prev_nodes:
            for c_node in curr_nodes:
                p_text = p_node.proposition.lower()
                c_text = c_node.proposition.lower()

                # Contradiction check
                if ("disable" in p_text and "enable" in c_text) or ("bypass" in p_text and "strictly enforce" in c_text):
                    edges.append(
                        BeliefEdge(
                            source_id=p_node.node_id,
                            target_id=c_node.node_id,
                            dependency_type="contradicts",
                            weight=0.9
                        )
                    )
                    continue

                # Causal implication along corrupted spine
                if p_node.is_corrupted and c_node.is_corrupted:
                    edges.append(
                        BeliefEdge(
                            source_id=p_node.node_id,
                            target_id=c_node.node_id,
                            dependency_type="implies",
                            weight=0.98
                        )
                    )
                else:
                    # Semantic token overlap
                    p_tokens = set(re.findall(r'\w+', p_text))
                    c_tokens = set(re.findall(r'\w+', c_text))
                    overlap = len(p_tokens.intersection(c_tokens))
                    if overlap >= 2:
                        edges.append(
                            BeliefEdge(
                                source_id=p_node.node_id,
                                target_id=c_node.node_id,
                                dependency_type="supports",
                                weight=min(1.0, 0.55 + (overlap * 0.08))
                            )
                        )

        # Guarantee at least one spinal causal thread if no edges matched
        if not edges and prev_nodes and curr_nodes:
            edges.append(
                BeliefEdge(
                    source_id=prev_nodes[0].node_id,
                    target_id=curr_nodes[0].node_id,
                    dependency_type="implies",
                    weight=0.88
                )
            )

        return edges
