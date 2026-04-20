"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.config import Settings
from src.api.models.base import Base

settings = Settings()

# Lazy initialization - engine is created only when needed
_engine = None
SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(settings.database_url)
    return _engine


def _get_session_local():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_get_engine())
    return SessionLocal


def get_db():
    session_local = _get_session_local()
    db = session_local()
    try:
        yield db
    finally:
        db.close()
