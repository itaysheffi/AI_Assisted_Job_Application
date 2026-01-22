import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    # Returning a dict ensures FastAPI serializes it as a JSON response.
    return {
        "status": "ok",
        "service": "AI Assisted Job Analyzer",
        "env": os.getenv("ENV", "development"),
    }

