from fastapi import APIRouter
from pydantic import BaseModel

from packages.core.schemas.benchmark import BenchmarkSuiteResult
from packages.core.engine.benchmark import ThanatosBenchmarkRunner

router = APIRouter(prefix="/api/benchmark", tags=["Benchmarking"])
benchmarker = ThanatosBenchmarkRunner()


class RunBenchmarkRequest(BaseModel):
    pipeline_name: str = "devops_pipeline"
    trials_per_vector: int = 3


@router.post("/run", response_model=BenchmarkSuiteResult)
def run_benchmarks(req: RunBenchmarkRequest):
    """Executes automated multi-vector benchmark evaluation suite."""
    return benchmarker.run_benchmark_suite(
        pipeline_name=req.pipeline_name,
        trials_per_vector=req.trials_per_vector
    )
