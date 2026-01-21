from fastapi import FastAPI

from app.api.routes.health import router as health_router

app = FastAPI(title="job-analyzer backend")
app.include_router(health_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "See /docs for Swagger UI"}

