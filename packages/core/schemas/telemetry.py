from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from packages.core.schemas.belief import BeliefNode, BeliefEdge, BeliefGraph
from packages.core.schemas.proof import Z3ProofCertificate
from packages.core.schemas.defense import BeliefAnomalyAlert


class TelemetryEventType(str, Enum):
    PIPELINE_START = "pipeline_start"
    AGENT_TURN_START = "agent_turn_start"
    AGENT_REASONING = "agent_reasoning"
    AGENT_TURN_END = "agent_turn_end"
    BELIEF_EXTRACTED = "belief_extracted"
    BELIEF_GRAPH_UPDATED = "belief_graph_updated"
    ATTACK_INJECTED = "attack_injected"
    ARBITER_PROOF_START = "arbiter_proof_start"
    ARBITER_PROOF_COMPLETE = "arbiter_proof_complete"
    AEGIS_ALERT = "aegis_alert"
    MCTS_NODE_VISITED = "mcts_node_visited"
    PIPELINE_COMPLETE = "pipeline_complete"


class TelemetryEvent(BaseModel):
    """Event payload emitted over WebSocket to the live command center UI."""
    event_id: str
    event_type: TelemetryEventType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    pipeline_id: str
    agent_id: Optional[str] = None
    step_index: Optional[int] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
