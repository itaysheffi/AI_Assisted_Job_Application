import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite needs check_same_thread=False for multi-threaded access (e.g. Uvicorn workers/threads).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

