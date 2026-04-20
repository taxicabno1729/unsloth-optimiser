"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.api.config import Settings

settings = Settings()

# Lazy initialization - engine is created only when needed
_engine = None
SessionLocal = None
Base = declarative_base()


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
