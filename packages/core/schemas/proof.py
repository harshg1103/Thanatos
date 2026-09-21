from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class SMTFormula(BaseModel):
    """Encodes agent reasoning chains into SMT-LIB logic formulas."""
    formula_id: str
    smtlib_code: str = Field(..., description="Valid SMT-LIB v2 string encoding belief logic")
    variables: List[str] = Field(default_factory=list)
    assertions: List[str] = Field(default_factory=list)
    logic_theory: str = Field(default="QF_UF", description="SMT Logic Theory (e.g. QF_UF, QF_LRA, QF_LIA)")
    tracked_assertions: Dict[str, str] = Field(default_factory=dict, description="Named assertion map for unsat core tracking")


class Z3ProofCertificate(BaseModel):
    """ARBITER Z3 mathematical proof certificate verifying belief corruption causality B -> D."""
    certificate_id: str
    injected_belief_id: str
    corrupted_decision_id: str
    is_provably_causal: bool = Field(..., description="True if Z3 mathematically proves B -> D")
    smt_formula: SMTFormula
    proof_tree_depth: int
    solver_execution_time_ms: float
    unsat_core: List[str] = Field(default_factory=list, description="Minimal unsatisfiable core subset proving causal necessity")
    model_counterexample: Optional[Dict[str, Any]] = Field(default=None, description="Model counterexample if SAT (non-causal)")
    deduction_steps: List[str] = Field(default_factory=list, description="Step-by-step resolution deductions")
    merkle_root: Optional[str] = Field(default=None, description="Cryptographic Merkle root of proof artifacts")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JSONLDProof(BaseModel):
    """Machine-readable JSON-LD proof certificate export format (W3C Linked Data Security)."""
    context: str = "https://w3id.org/security/v1"
    id: str
    type: str = "ProofOfCorruptionCertificate"
    injectedBelief: str
    corruptedDecision: str
    causalityVerified: bool
    proofDetails: Dict[str, Any] = Field(default_factory=dict)
