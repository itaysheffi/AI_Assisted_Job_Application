import os

from fastapi import APIRouter

from app.db.session import db_check

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    # Returning a dict ensures FastAPI serializes it as a JSON response.
    return {
        "status": "ok",
        "service": "AI Assisted Job Analyzer",
        "env": os.getenv("ENV", "development"),
    }


@router.get("/health/db")
def health_db() -> dict[str, str]:
    db_check()
    return {"status": "ok"}

