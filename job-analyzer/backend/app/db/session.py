from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


# SQLite needs check_same_thread=False for multi-threaded access (e.g. Uvicorn workers/threads).
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a DB session with rollback/close safety."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def db_check() -> None:
    """Raise if DB is unreachable; used by health checks."""
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
