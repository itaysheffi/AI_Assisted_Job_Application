from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from a local `.env` file into `os.environ` early.
# This keeps configuration consistent across local dev, tests, and deployment.
DOTENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=DOTENV_PATH, override=True)

from fastapi import APIRouter, FastAPI  # noqa: E402 (intentional import after load_dotenv)

from app.api.health import router as health_router
from app.core.config import settings

placeholder_router = APIRouter()


def create_app() -> FastAPI:
    """App factory (best practice for testing and reuse)."""
    app = FastAPI(title="AI Assisted Job Analyzer")

    # Placeholder router: we'll add real routes later.
    app.include_router(placeholder_router)
    app.include_router(health_router)

    # TEMP (dev-only): remove this route before production.
    if settings.env == "development" or settings.debug:
        from app.api.routes.debug import router as debug_router

        app.include_router(debug_router)

    @app.get("/")
    def root() -> dict[str, str]:
        return {"message": "See /docs for Swagger UI"}

    return app


app = create_app()

