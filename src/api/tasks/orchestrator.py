"""Task orchestration layer that coordinates between API and Celery workers."""
from src.api.schemas.task import TaskCreate, OptimizationMethod
from src.api.tasks.celery import celery_app as app


class TaskOrchestrator:
    """Orchestrates optimization tasks between API and Celery workers."""

    def __init__(self):
        self.worker_mapping = {
            OptimizationMethod.QUANTIZATION: "optimization_worker.process_quantization",
            OptimizationMethod.LORA: "optimization_worker.process_lora",
            OptimizationMethod.AWQ: "optimization_worker.process_awq",
            OptimizationMethod.GPTQ: "optimization_worker.process_gptq",
        }

    def validate_config(self, config: TaskCreate) -> bool:
        """Validate optimization configuration.

        Args:
            config: Task creation schema containing task configuration

        Returns:
            True if configuration is valid, False otherwise
        """
        if not config.name or len(config.name) < 1:
            return False
        if not config.model_name or len(config.model_name) < 1:
            return False
        if config.optimization_method not in self.worker_mapping:
            return False
        return True

    def schedule_task(self, task_config: TaskCreate, task_id: str) -> str:
        """Schedule optimization task to appropriate worker.

        Args:
            task_config: Task creation configuration
            task_id: Unique identifier for the task

        Returns:
            Celery task ID string

        Raises:
            ValueError: If task configuration is invalid or no worker available
        """
        if not self.validate_config(task_config):
            raise ValueError("Invalid task configuration")

        worker_task_name = self.worker_mapping.get(task_config.optimization_method)
        if not worker_task_name:
            raise ValueError(f"No worker available for method: {task_config.optimization_method}")

        # Send task to Celery worker
        result = app.send_task(
            worker_task_name,
            kwargs={"config": task_config.model_dump()}
        )
        return result.id
