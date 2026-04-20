"""Unsloth Optimiser API - Main FastAPI application."""

from datetime import datetime
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, Request
from src.api.routers import auth, tasks
from src.api.config import Settings
from src.api.tasks.celery import celery_app
from src.api.tasks.orchestrator import TaskOrchestrator
from src.api.monitoring.health import router as health_router
from src.api.monitoring.metrics import MetricsMiddleware, get_metrics
import json

settings = Settings()

app = FastAPI(
    title="Unsloth Optimiser API",
    description="Web-based optimization interface for Unsloth library",
    version="0.1.0"
)

# Add metrics middleware
app.add_middleware(MetricsMiddleware)


@app.on_event("startup")
async def startup_event():
    """Startup event handler - add Celery and orchestrator to app state."""
    app.state.celery_app = celery_app
    app.state.orchestrator = TaskOrchestrator()


# Include routers
app.include_router(auth.router, prefix=settings.api_v1_prefix, tags=["auth"])
app.include_router(tasks.router, prefix=settings.api_v1_prefix, tags=["tasks"])
app.include_router(health_router, prefix=settings.api_v1_prefix, tags=["health"])


# Metrics endpoint (not under /api/v1/)
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return get_metrics()


# Simple health endpoint at root for backward compatibility
@app.get("/health")
async def root_health_check():
    """Simple health check at root for backward compatibility."""
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "healthy"}


@app.websocket("/ws/tasks/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    try:
        # Send initial connection message
        await websocket.send_text(json.dumps({
            "task_id": task_id,
            "status": "connected",
            "message": "WebSocket connection established"
        }))
        
        while True:
            # Receive and echo back with task_id
            data = await websocket.receive_text()
            await websocket.send_text(json.dumps({
                "task_id": task_id,
                "status": "update",
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }))
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(json.dumps({
            "task_id": task_id,
            "status": "error",
            "error": str(e)
        }))
