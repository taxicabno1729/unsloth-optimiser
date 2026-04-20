"""Result model for optimization results."""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from src.db.models.base import BaseModel


class Result(BaseModel):
    """Model for storing optimization results."""
    __tablename__ = "results"

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    metrics = Column(JSON, nullable=False)
    output_path = Column(String(512), nullable=True)
    error_log = Column(Text, nullable=True)

    # Relationship
    task = relationship("Task", back_populates="result")

    def __repr__(self):
        return f"<Result(task_id={self.task_id})>"