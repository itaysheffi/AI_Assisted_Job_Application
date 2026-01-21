from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    # Returning a dict ensures FastAPI serializes it as a JSON response.
    return {"status": "ok", "service": settings.app_name, "env": settings.env}

