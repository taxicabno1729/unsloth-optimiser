"""Celery app configuration for distributed task processing."""

from celery import Celery

from src.api.config import Settings

settings = Settings()

celery_app = Celery(
    "unsloth-optimiser-worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    worker_prefetch_multiplier=1,
)
