from fastapi import APIRouter, HTTPException

from app.core.config import settings

router = APIRouter(prefix="/debug", tags=["debug"])


# TEMP (dev-only): remove these debug endpoints later.
@router.get("/config")
def debug_config() -> dict[str, object]:
    # Defense in depth: even though this router is only included in development,
    # refuse access if it's ever mounted in production by mistake.
    if not (settings.env == "development" or settings.debug):
        raise HTTPException(status_code=404, detail="Not Found")
    return {"has_openai_key": bool(settings.openai_api_key), "env": settings.env}

