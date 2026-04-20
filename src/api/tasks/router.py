"""Task management API router."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.db.config.database import get_db_session
from src.db.models.task import Task as TaskModel
from src.db.models.optimization_config import OptimizationConfig
from src.api.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db_session)
):
    """Create a new task."""
    # Verify the config exists
    config = db.query(OptimizationConfig).filter(OptimizationConfig.id == task.config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    # Create the task
    db_task = TaskModel(
        config_id=task.config_id,
        status=task.status,
        progress=task.progress,
        error_message=task.error_message
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db_session)
):
    """Get a specific task by ID."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=TaskListResponse)
def list_tasks(
    db: Session = Depends(get_db_session),
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """List all tasks with optional filtering and pagination."""
    query = db.query(TaskModel)
    
    # Apply status filter if provided
    if status:
        query = query.filter(TaskModel.status == status)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    tasks = query.order_by(desc(TaskModel.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "items": tasks,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.put("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db_session)
):
    """Update task status and progress."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update fields if provided
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.progress is not None:
        task.progress = task_update.progress
    if task_update.error_message is not None:
        task.error_message = task_update.error_message
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=200)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db_session)
):
    """Delete a task."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
