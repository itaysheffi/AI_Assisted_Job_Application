## job-analyzer

Analyzes job posts (and related inputs) and exposes backend APIs to support an AI-assisted job application workflow.

### Backend (FastAPI + SQLite)

#### Run locally

```bash
cd backend

# create venv
python -m venv .venv

# activate venv (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# (macOS/Linux)
# source .venv/bin/activate

# install deps
pip install -r requirements.txt

# env file
cp .env.example .env
# (Windows PowerShell alternative)
# Copy-Item .env.example .env

# run
uvicorn app.main:app --reload
```

Then open:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
- Users: `http://127.0.0.1:8000/users`
- Jobs: `http://127.0.0.1:8000/jobs`

Notes:
- Settings are loaded from `backend/.env` (optional) and environment variables.
- Key variables:
  - `ENV`: `development` (default), `staging`, `production`
  - `DATABASE_URL`: defaults to SQLite for local dev; **must be non-SQLite in prod/staging**
  - `SECRET_KEY`: dev default is provided; **must be set in prod/staging**
- `OPENAI_API_KEY` is optional (some features may require it).

