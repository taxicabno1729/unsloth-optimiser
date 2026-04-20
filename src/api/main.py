"""Unsloth Optimiser API - Main FastAPI application."""

from fastapi import FastAPI

app = FastAPI(
    title="Unsloth Optimiser API",
    description="Web-based optimization interface for Unsloth library",
    version="0.1.0"
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
