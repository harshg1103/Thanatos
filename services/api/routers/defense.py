from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel

from packages.core.schemas.belief import BeliefGraph
from packages.core.schemas.defense import DefenseEvaluationReport
from packages.core.engine.aegis import AegisDefenseEngine
from packages.core.engine.compliance import ComplianceMapper

router = APIRouter(prefix="/api/defense", tags=["AEGIS Defense & Compliance"])
aegis = AegisDefenseEngine()


class DefenseAuditRequest(BaseModel):
    pipeline_name: str = "devops_pipeline"
    belief_graph: BeliefGraph
    execution_turns: List[Dict[str, Any]] = []


@router.post("/evaluate", response_model=DefenseEvaluationReport)
def evaluate_defense(req: DefenseAuditRequest):
    """AEGIS Real-time Defense Evaluation: detects anomalies, semantic drift, and computes integrity score."""
    return aegis.evaluate_pipeline_run(
        pipeline_name=req.pipeline_name,
        belief_graph=req.belief_graph,
        execution_turns=req.execution_turns
    )


@router.get("/compliance-matrix")
def get_compliance_matrix():
    """Returns OWASP Top 10 for LLMs and MITRE ATLAS security taxonomy mapping."""
    return ComplianceMapper.get_full_taxonomy_matrix()
