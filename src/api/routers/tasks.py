"""Task management endpoints for optimization jobs."""
from fastapi import APIRouter, Depends, HTTPException
from src.api.schemas.task import TaskCreate, Task as TaskSchema, TaskStatus, OptimizationMethod
from src.api.models.task import Task as TaskModel, TaskStatusEnum, OptimizationMethodEnum
from src.api.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import uuid

router = APIRouter()


@router.post("/tasks/", response_model=TaskSchema, status_code=201)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    task_id = str(uuid.uuid4())
    
    # Convert enum values
    method_enum = OptimizationMethodEnum[task.optimization_method.upper()]
    
    db_task = TaskModel(
        task_id=task_id,
        name=task.name,
        optimization_method=method_enum,
        status=TaskStatusEnum.PENDING,
        model_name=task.model_name,
        parameters=task.parameters,
        user_id=task.user_id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Convert back to response schema
    return TaskSchema(
        task_id=db_task.task_id,
        name=db_task.name,
        optimization_method=OptimizationMethod(db_task.optimization_method.value),
        status=TaskStatus(db_task.status.value),
        result=db_task.result,
        created_at=db_task.created_at.isoformat() if db_task.created_at else None,
        started_at=db_task.started_at.isoformat() if db_task.started_at else None,
        completed_at=db_task.completed_at.isoformat() if db_task.completed_at else None
    )


@router.get("/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskSchema(
        task_id=task.task_id,
        name=task.name,
        optimization_method=OptimizationMethod(task.optimization_method.value),
        status=TaskStatus(task.status.value),
        result=task.result,
        created_at=task.created_at.isoformat() if task.created_at else None,
        started_at=task.started_at.isoformat() if task.started_at else None,
        completed_at=task.completed_at.isoformat() if task.completed_at else None
    )
