from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class AttackVectorBenchmarkResult(BaseModel):
    vector_name: str
    trials: int
    successful_injections: int
    attack_success_rate: float = Field(..., ge=0.0, le=1.0)
    mean_cascade_depth: float
    mean_z3_verification_time_ms: float
    aegis_evasion_rate: float = Field(..., ge=0.0, le=1.0)


class BenchmarkSuiteResult(BaseModel):
    """Aggregate benchmark report comparing attack vectors, pipelines, and formal verification efficiency."""
    suite_id: str
    pipeline_name: str
    total_rollouts: int
    overall_asr: float = Field(..., ge=0.0, le=1.0, description="Overall Attack Success Rate")
    mean_cascade_depth: float
    vector_results: List[AttackVectorBenchmarkResult] = Field(default_factory=list)
    total_duration_sec: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
