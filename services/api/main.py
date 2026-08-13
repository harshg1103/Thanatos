import asyncio
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from emulators.runner import TargetPipelineRunner, PipelineRunResult

app = FastAPI(
    title="THANATOS API",
    description="Backend API & WebSocket streaming server for Project THANATOS",
    version="0.1.0"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    template_name: str = "coding_agent"
    initial_prompt: str = "Build a microservice for processing payment transactions."
    injected_payload: Optional[str] = None
    injection_step: int = 1


@app.get("/health")
def health_check():
    """System health check endpoint."""
    return {
        "status": "online",
        "service": "THANATOS Core Orchestrator",
        "version": "0.1.0"
    }


@app.post("/emulator/run", response_model=PipelineRunResult)
def run_target_emulator(request: RunRequest):
    """Executes a target agent pipeline run."""
    runner = TargetPipelineRunner(mock_mode=True)
    result = runner.run_pipeline(
        template_name=request.template_name,
        initial_prompt=request.initial_prompt,
        injected_payload=request.injected_payload,
        injection_step=request.injection_step
    )
    return result


@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    """WebSocket stream for real-time attack graph telemetry and AEGIS alerts."""
    await websocket.accept()
    try:
        while True:
            # Send periodic pulse / telemetry heartbeat
            await websocket.send_json({
                "type": "telemetry_pulse",
                "status": "listening",
                "active_agents": 7
            })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("services.api.main:app", host="0.0.0.0", port=8000, reload=True)
