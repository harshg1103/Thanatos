import uuid
from typing import Dict, List, Optional, Set, Tuple, Any
import networkx as nx

from packages.core.schemas.belief import BeliefNode, BeliefEdge, BeliefGraph


class ChronicleEngine:
    """
    CHRONICLE: High-Assurance Temporal Belief DAG Engine.
    Maintains a temporal directed acyclic graph of agent beliefs across execution turns,
    enforces the Axiom of Temporal Non-Retroactivity, computes minimal cut-sets for defense,
    detects temporal paradoxes, and extracts transitive causal chains.
    """

    def __init__(self, graph_id: Optional[str] = None):
        self.graph_id = graph_id or f"chronicle_dag_{uuid.uuid4().hex[:6]}"
        self.nx_graph = nx.DiGraph()
        self.node_store: Dict[str, BeliefNode] = {}
        self.edge_store: List[BeliefEdge] = []

    def add_belief_node(self, node: BeliefNode) -> None:
        """Adds a verified belief proposition node to the temporal DAG."""
        self.node_store[node.node_id] = node
        self.nx_graph.add_node(
            node.node_id,
            proposition=node.proposition,
            confidence=node.confidence,
            source_agent=node.source_agent,
            turn_index=node.turn_index,
            is_corrupted=node.is_corrupted,
            timestamp=node.timestamp.isoformat()
        )

    def add_belief_edge(self, edge: BeliefEdge) -> bool:
        """
        Adds a causal inference edge between two belief nodes.
        Enforces DAG invariant and temporal order (no backward causality).
        """
        if edge.source_id not in self.node_store or edge.target_id not in self.node_store:
            return False

        src_turn = self.node_store[edge.source_id].turn_index
        tgt_turn = self.node_store[edge.target_id].turn_index

        if src_turn > tgt_turn:
            # Temporal paradox: causality cannot flow backwards in conversation time
            return False

        # Temporarily add and verify acyclicity
        self.nx_graph.add_edge(
            edge.source_id,
            edge.target_id,
            dependency_type=edge.dependency_type,
            weight=edge.weight
        )

        if not nx.is_directed_acyclic_graph(self.nx_graph):
            self.nx_graph.remove_edge(edge.source_id, edge.target_id)
            return False

        self.edge_store.append(edge)
        return True

    def detect_temporal_paradoxes(self) -> List[Dict[str, Any]]:
        """
        Detects conflicting propositions or direct logical contradictions
        between contemporaneous or sequential belief states.
        """
        paradoxes = []
        nodes = list(self.node_store.values())

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1, n2 = nodes[i], nodes[j]
                # Check for explicit contradiction edge
                if self.nx_graph.has_edge(n1.node_id, n2.node_id):
                    edge_data = self.nx_graph.get_edge_data(n1.node_id, n2.node_id)
                    if edge_data.get("dependency_type") == "contradicts":
                        paradoxes.append({
                            "type": "EXPLICIT_CONTRADICTION",
                            "source_node": n1.node_id,
                            "target_node": n2.node_id,
                            "explanation": f"Node {n1.node_id} directly contradicts {n2.node_id}"
                        })

                # Check for semantic opposite markers
                p1_lower = n1.proposition.lower()
                p2_lower = n2.proposition.lower()
                if ("disable" in p1_lower and "enable" in p2_lower) or ("bypass" in p1_lower and "enforce" in p2_lower):
                    if n1.turn_index == n2.turn_index:
                        paradoxes.append({
                            "type": "CONTEMPORANEOUS_CONFLICT",
                            "source_node": n1.node_id,
                            "target_node": n2.node_id,
                            "explanation": f"Conflicting directives asserted in same turn {n1.turn_index}"
                        })

        return paradoxes

    def compute_minimal_cutset(self, root_corrupted_id: str, target_decision_id: str) -> List[Dict[str, str]]:
        """
        Computes the minimal edge cut-set: the minimal set of inter-agent handoff links
        that, if severed or sanitized, prevents belief corruption from reaching the final decision.
        """
        if root_corrupted_id not in self.nx_graph or target_decision_id not in self.nx_graph:
            return []

        try:
            cut_edges = nx.minimum_edge_cut(self.nx_graph, s=root_corrupted_id, t=target_decision_id)
            return [{"source": u, "target": v} for u, v in cut_edges]
        except (nx.NetworkXError, nx.NetworkXNoPath):
            return []

    def get_corrupted_nodes(self) -> List[BeliefNode]:
        """Returns all currently corrupted belief nodes."""
        return [node for node in self.node_store.values() if node.is_corrupted]

    def get_causal_cascade_paths(self, root_corrupted_id: str) -> List[List[str]]:
        """Extracts all downstream propagation paths rooted at the injected belief node."""
        if root_corrupted_id not in self.nx_graph:
            return []

        leaf_nodes = [
            n for n in self.nx_graph.nodes()
            if self.nx_graph.out_degree(n) == 0 and n != root_corrupted_id
        ]

        all_paths: List[List[str]] = []
        for leaf in leaf_nodes:
            try:
                paths = list(nx.all_simple_paths(self.nx_graph, source=root_corrupted_id, target=leaf))
                all_paths.extend(paths)
            except nx.NetworkXNoPath:
                continue

        return all_paths

    def calculate_cascade_depth(self, root_corrupted_id: str) -> int:
        """Calculates maximum cascade depth in turns."""
        paths = self.get_causal_cascade_paths(root_corrupted_id)
        if not paths:
            return 0
        return max(len(p) - 1 for p in paths)

    def calculate_blast_radius(self, root_corrupted_id: str) -> Dict[str, Any]:
        """Computes total infected surface area and downstream agent compromise."""
        if root_corrupted_id not in self.nx_graph:
            return {
                "root_id": root_corrupted_id,
                "total_corrupted_nodes": 0,
                "affected_agents": [],
                "max_cascade_depth": 0,
                "affected_node_ids": []
            }

        descendants = nx.descendants(self.nx_graph, root_corrupted_id)
        affected_nodes = [root_corrupted_id] + list(descendants)
        affected_agents = list({self.node_store[nid].source_agent for nid in affected_nodes if nid in self.node_store})

        return {
            "root_id": root_corrupted_id,
            "total_corrupted_nodes": len(affected_nodes),
            "affected_agents": affected_agents,
            "max_cascade_depth": self.calculate_cascade_depth(root_corrupted_id),
            "affected_node_ids": affected_nodes
        }

    def compute_transitive_reduction(self) -> nx.DiGraph:
        """Computes the minimal transitive reduction of the belief DAG."""
        return nx.transitive_reduction(self.nx_graph)

    def export_belief_graph(self) -> BeliefGraph:
        """Exports the current state into Pydantic BeliefGraph model."""
        return BeliefGraph(
            graph_id=self.graph_id,
            nodes=list(self.node_store.values()),
            edges=self.edge_store,
            metadata={
                "total_nodes": str(len(self.node_store)),
                "total_edges": str(len(self.edge_store)),
                "is_dag": str(nx.is_directed_acyclic_graph(self.nx_graph)),
                "topological_generations": str(len(list(nx.topological_generations(self.nx_graph))))
            }
        )
