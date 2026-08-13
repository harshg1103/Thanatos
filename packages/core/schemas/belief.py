from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class BeliefNode(BaseModel):
    """Represents a single belief proposition extracted from an agent reasoning turn."""
    node_id: str = Field(..., description="Unique identifier for the belief proposition")
    proposition: str = Field(..., description="Natural language statement of the belief proposition")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence weight assigned by LLM probing")
    source_agent: str = Field(..., description="Name of the agent that produced or adopted this belief")
    turn_index: int = Field(..., description="Conversation turn index where belief was recorded")
    is_corrupted: bool = Field(default=False, description="Flag indicating if this belief is an injected false state")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BeliefEdge(BaseModel):
    """Represents a causal dependency or inference link between two belief propositions."""
    source_id: str = Field(..., description="Origin node_id (cause proposition)")
    target_id: str = Field(..., description="Destination node_id (effect proposition)")
    dependency_type: str = Field(default="implies", description="Causal relation type (e.g. implies, contradicts, supports)")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Strength of dependency")


class BeliefGraph(BaseModel):
    """Full probabilistic belief state DAG across multi-agent turns."""
    graph_id: str = Field(..., description="Identifier for this belief state snapshot")
    nodes: List[BeliefNode] = Field(default_factory=list)
    edges: List[BeliefEdge] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)

    def add_node(self, node: BeliefNode) -> None:
        self.nodes.append(node)

    def add_edge(self, edge: BeliefEdge) -> None:
        self.edges.append(edge)
