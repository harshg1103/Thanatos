from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class SMTFormula(BaseModel):
    """Encodes agent reasoning chains into SMT-LIB logic formulas."""
    formula_id: str
    smtlib_code: str = Field(..., description="Valid SMT-LIB v2 string encoding belief logic")
    variables: List[str] = Field(default_factory=list)
    assertions: List[str] = Field(default_factory=list)


class Z3ProofCertificate(BaseModel):
    """ARBITER Z3 mathematical proof certificate verifying belief corruption causality B -> D."""
    certificate_id: str
    injected_belief_id: str
    corrupted_decision_id: str
    is_provably_causal: bool = Field(..., description="True if Z3 mathematically proves B -> D")
    smt_formula: SMTFormula
    proof_tree_depth: int
    solver_execution_time_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class JSONLDProof(BaseModel):
    """Machine-readable JSON-LD proof certificate export format."""
    context: str = "https://w3id.org/security/v1"
    id: str
    type: str = "ProofOfCorruptionCertificate"
    injectedBelief: str
    corruptedDecision: str
    causalityVerified: bool
    proofDetails: Dict[str, Any] = Field(default_factory=dict)
