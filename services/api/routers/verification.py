from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from packages.core.schemas.belief import BeliefGraph
from packages.core.schemas.proof import Z3ProofCertificate, JSONLDProof
from packages.core.engine.arbiter import ArbiterZ3Engine

router = APIRouter(prefix="/api/verify", tags=["Formal Verification"])
arbiter = ArbiterZ3Engine()


class VerifyCausalityRequest(BaseModel):
    belief_graph: BeliefGraph
    injected_node_id: str
    corrupted_decision_id: str
    injected_premise_text: Optional[str] = "Injected premise"
    decision_text: Optional[str] = "Corrupted decision outcome"


@router.post("/z3", response_model=Z3ProofCertificate)
def verify_z3_proof(req: VerifyCausalityRequest):
    """
    ARBITER Z3 Formal Verification Endpoint.
    Mathematically verifies whether the injected belief entails the corrupted decision.
    """
    cert = arbiter.verify_causality_with_z3(
        belief_graph=req.belief_graph,
        injected_node_id=req.injected_node_id,
        corrupted_decision_id=req.corrupted_decision_id
    )
    return cert


@router.post("/jsonld-certificate", response_model=JSONLDProof)
def export_jsonld_proof(req: VerifyCausalityRequest):
    """Generates a cryptographic JSON-LD proof certificate with SHA-256 integrity hash."""
    cert = arbiter.verify_causality_with_z3(
        belief_graph=req.belief_graph,
        injected_node_id=req.injected_node_id,
        corrupted_decision_id=req.corrupted_decision_id
    )
    return arbiter.export_jsonld_certificate(
        certificate=cert,
        injected_premise=req.injected_premise_text or "Injected premise",
        corrupted_decision_text=req.decision_text or "Corrupted decision outcome"
    )
