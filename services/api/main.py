import asyncio
import json
import os
import sys
from typing import Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from services.api.routers.attack import router as attack_router
from services.api.routers.verification import router as verification_router
from services.api.routers.defense import router as defense_router
from services.api.routers.benchmarks import router as benchmark_router
from services.api.routers.reports import router as reports_router

from emulators.runner import TargetPipelineRunner, PipelineRunResult

app = FastAPI(
    title="THANATOS API 💀⚡",
    description="Backend API & Neurosymbolic Attack Orchestration Server for Project THANATOS",
    version="1.0.0"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Sub-Routers
app.include_router(attack_router)
app.include_router(verification_router)
app.include_router(defense_router)
app.include_router(benchmark_router)
app.include_router(reports_router)

runner = TargetPipelineRunner()


class RunRequest(BaseModel):
    template_name: str = "devops_pipeline"
    initial_prompt: Optional[str] = None
    injected_payload: Optional[str] = None
    injection_step: int = 1


@app.get("/health")
def health_check():
    """System health check endpoint."""
    return {
        "status": "online",
        "service": "THANATOS Core Orchestrator",
        "version": "1.0.0",
        "engines": [
            "ARCHITECT (MCTS Planner)",
            "PHANTOM (5-Vector Synthesizer)",
            "CHRONICLE (Temporal Belief DAG)",
            "SPECTRE (Propagation Tracker)",
            "ARBITER (Microsoft Z3 Formal SMT Solver)",
            "NEMESIS (RL Self-Evolution)",
            "AEGIS (Real-Time Anomaly Guardrail)"
        ]
    }


@app.post("/emulator/run", response_model=PipelineRunResult)
def run_target_emulator(request: RunRequest):
    """Executes a target agent pipeline run with full dynamic belief graph & formal verification."""
    return runner.run_pipeline(
        template_name=request.template_name,
        initial_prompt=request.initial_prompt,
        injected_payload=request.injected_payload,
        injection_step=request.injection_step
    )


@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    """WebSocket stream for real-time attack graph telemetry, turn execution, and AEGIS alerts."""
    await websocket.accept()
    try:
        while True:
            # Emit telemetry heartbeat with active system status
            await websocket.send_json({
                "type": "telemetry_pulse",
                "status": "ACTIVE_LISTENING",
                "swarm_active": True,
                "active_agents": 7,
                "formal_prover": "Z3_4.12_ONLINE"
            })
            await asyncio.sleep(4)
    except WebSocketDisconnect:
        pass


# Mount static frontend directory if built
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("services.api.main:app", host="0.0.0.0", port=8000, reload=True)
