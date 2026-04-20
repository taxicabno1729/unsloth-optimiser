"""Unsloth Optimiser API - Main FastAPI application."""

from fastapi import FastAPI, Depends
from src.api.routers import auth, tasks
from src.api.config import Settings

settings = Settings()

app = FastAPI(
    title="Unsloth Optimiser API",
    description="Web-based optimization interface for Unsloth library",
    version="0.1.0"
)

# Include auth router
app.include_router(auth.router, prefix=settings.api_v1_prefix, tags=["auth"])
app.include_router(tasks.router, prefix=settings.api_v1_prefix, tags=["tasks"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
