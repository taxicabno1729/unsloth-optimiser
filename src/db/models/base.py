"""Base model for all database models."""
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from src.db.config.database import Base


class BaseModel(Base):
    """Base class for all models with common fields."""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())