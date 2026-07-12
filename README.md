# Atlas AI

Atlas AI is an AI-powered business operating system for discovering, evaluating, and ranking online business opportunities.

## Project Structure

- `backend/`: FastAPI API, services, repositories, SQLAlchemy models, Alembic migrations, and backend tests.
- `frontend/`: Next.js founder dashboard for evaluating opportunity portfolios.
- `docs/`: API, sprint, changelog, architecture, decision, and database documentation.
- `knowledge/`: business intelligence notes. This is not executable code.

## Backend Setup

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Run the backend:

```powershell
.\.venv\Scripts\uvicorn.exe app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

Backend verification:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests
.\.venv\Scripts\python.exe -m compileall -q backend\app backend\tests backend\migrations
.\.venv\Scripts\alembic.exe -c backend\alembic.ini upgrade head --sql
```

## Frontend Setup

```powershell
Set-Location frontend
npm.cmd install
Copy-Item .env.example .env.local
```

Run the founder dashboard:

```powershell
npm.cmd run dev
```

Open:

```text
http://localhost:3000
```

Frontend verification:

```powershell
npm.cmd run typecheck
npm.cmd run lint
npm.cmd run build
```

The dashboard calls:

```text
http://127.0.0.1:8000/api/v1/opportunities/portfolio
```
