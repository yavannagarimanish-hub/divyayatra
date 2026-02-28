# divyayatra
Devotional Trip Planner for India

## Backend setup (FastAPI)

The backend now includes a modular FastAPI application with:
- database connection setup (`backend/database.py`)
- temple SQLAlchemy model (`backend/models/temple.py`)
- temple API routes (`backend/routes/temples.py`)
- app entrypoint (`backend/main.py`)

### Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Environment variable

Use `DATABASE_URL` to override the default SQLite database:

```bash
export DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/divyayatra"
```
