import logging

from fastapi import FastAPI

from app.api.routes import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """App factory (best practice for testing and reuse)."""
    app = FastAPI(title="AI Assisted Job Analyzer")

    app.include_router(api_router)

    @app.on_event("startup")
    async def _log_settings_loaded() -> None:
        # Confirm settings loaded without ever logging secrets.
        logger.info(
            "Settings loaded env=%s debug=%s database=%s secret_key_set=%s dotenv_files=%s",
            settings.ENV,
            settings.DEBUG,
            settings.safe_database_target(),
            bool(settings.SECRET_KEY),
            settings.dotenv_file_status(),
        )

    # TEMP (dev-only): remove this route before production.
    if settings.env == "development" or settings.debug:
        from app.api.routes.debug import router as debug_router

        app.include_router(debug_router)

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "See /docs for Swagger UI"}

    return app


app = create_app()

