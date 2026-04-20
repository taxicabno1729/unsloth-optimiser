"""Health check endpoints for the Unsloth Optimiser API."""
from fastapi import APIRouter
from datetime import datetime, timezone
from src.api.config import Settings

settings = Settings()
router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "0.1.0",
        "service": settings.project_name
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes."""
    # TODO: Check database and Redis connectivity
    return {
        "status": "ready",
        "checks": {
            "database": "ok",
            "redis": "ok"
        }
    }
