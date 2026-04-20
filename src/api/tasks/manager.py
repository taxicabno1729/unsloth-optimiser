"""Task manager for database operations and task lifecycle management."""
from sqlalchemy.orm import Session
from src.api.database import get_db
from src.api.schemas.task import TaskCreate, TaskStatus
from src.api.models.task import Task as TaskModel, TaskStatusEnum, OptimizationMethodEnum
from typing import List, Optional


class TaskManager:
    """Manages task records in the database and task lifecycle."""

    def __init__(self):
        self.db_generator = get_db

    def _get_db(self) -> Session:
        """Get database session.

        Returns:
            SQLAlchemy session object
        """
        return next(self.db_generator())

    def create_task_record(
        self,
        task_data: TaskCreate,
        task_id: str,
        celery_task_id: str = None
    ) -> TaskModel:
        """Create task record in database.

        Args:
            task_data: Task creation schema
            task_id: Unique task identifier
            celery_task_id: Optional Celery task ID

        Returns:
            Created Task model instance
        """
        db = self._get_db()
        try:
            db_task = TaskModel(
                task_id=task_id,
                name=task_data.name,
                optimization_method=OptimizationMethodEnum(task_data.optimization_method.value),
                status=TaskStatusEnum.PENDING,
                model_name=task_data.model_name,
                parameters=task_data.parameters,
                user_id=task_data.user_id,
                celery_task_id=celery_task_id
            )
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return db_task
        finally:
            db.close()

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: dict = None
    ) -> Optional[TaskModel]:
        """Update task status in database.

        Args:
            task_id: Unique task identifier
            status: New task status
            result: Optional result dictionary

        Returns:
            Updated Task model instance or None if not found
        """
        db = self._get_db()
        try:
            task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
            if task:
                task.status = TaskStatusEnum(status.value)
                if result:
                    task.result = result
                db.commit()
                return task
            return None
        finally:
            db.close()

    def get_task_history(
        self,
        user_id: str = None,
        limit: int = 100
    ) -> List[TaskModel]:
        """Retrieve task history.

        Args:
            user_id: Optional user ID to filter by
            limit: Maximum number of tasks to return

        Returns:
            List of Task model instances
        """
        db = self._get_db()
        try:
            query = db.query(TaskModel)
            if user_id:
                query = query.filter(TaskModel.user_id == user_id)
            return query.order_by(TaskModel.created_at.desc()).limit(limit).all()
        finally:
            db.close()

    def get_task_by_id(self, task_id: str) -> Optional[TaskModel]:
        """Get task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task model instance or None if not found
        """
        db = self._get_db()
        try:
            return db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
        finally:
            db.close()
