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

