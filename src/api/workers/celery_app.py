"""Celery tasks for distributed task processing."""

from src.api.tasks.celery import celery_app


@celery_app.task(bind=True, max_retries=3)
def process_task(self, task_data: dict):
    """Process optimization task with retry mechanism.

    Args:
        task_data: Dictionary containing task configuration

    Returns:
        Dictionary with task_id, status, result and method

    Raises:
        Retries the task after 60 seconds on exception
    """
    try:
        method = task_data.get("optimization_method")
        task_id = task_data.get("task_id")

        # TODO: Implement actual optimization logic
        return {
            "task_id": task_id,
            "status": "completed",
            "result": f"Optimized with {method}",
            "method": method
        }
    except Exception as exc:
        # Retry after 60 seconds
        self.retry(exc=exc, countdown=60)
