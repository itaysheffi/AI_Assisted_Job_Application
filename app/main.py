from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.db.base import Base
from app.db.session import engine
import app.models  # noqa: F401  (ensures models are imported for metadata)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Simple dev-friendly approach: create tables on startup (no migrations).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="FastAPI Modular + SQLite", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "See /docs for Swagger UI"}

