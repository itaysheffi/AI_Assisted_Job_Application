## FastAPI + SQLite (modular routing)

### What you get
- **FastAPI app** with versioned, modular routing under `app/api/v1/routers/`
- **SQLite** persistence via **SQLAlchemy 2.0**
- Example CRUD resource: `Item`

### Setup
Create and activate a virtual environment, then install deps:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
uvicorn app.main:app --reload
```

Then open:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

### Project layout
- `app/main.py`: app entrypoint + router wiring
- `app/core/config.py`: settings (DB URL)
- `app/db/`: SQLAlchemy engine/session/base
- `app/models/`: ORM models
- `app/schemas/`: Pydantic DTOs
- `app/crud/`: DB operations
- `app/api/v1/routers/`: modular route modules

