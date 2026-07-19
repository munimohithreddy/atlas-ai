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

Business planner verification:

```powershell
.\.venv\Scripts\python.exe -m unittest backend.tests.test_brands backend.tests.test_business_planning
```

Campaign verification:

```powershell
.\.venv\Scripts\python.exe -m unittest backend.tests.test_campaigns backend.tests.test_migration_imports
.\.venv\Scripts\alembic.exe -c backend\alembic.ini upgrade head
```

Migration inspection:

```powershell
.\.venv\Scripts\alembic.exe -c backend\alembic.ini heads
.\.venv\Scripts\alembic.exe -c backend\alembic.ini current
.\.venv\Scripts\alembic.exe -c backend\alembic.ini history
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

The business-plan action also calls:

```text
http://127.0.0.1:8000/api/v1/opportunities/{opportunity_id}/business-plan
```

The campaign action also calls:

```text
http://127.0.0.1:8000/api/v1/campaigns
http://127.0.0.1:8000/api/v1/campaigns/{campaign_id}
```

## Manual Workflow

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests
.\.venv\Scripts\uvicorn.exe app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
Set-Location frontend
npm.cmd run dev
```

Git examples:

```powershell
git add .
git commit -m "Add campaign foundation"
git push origin main
git merge main
git tag v0.1.0-campaigns
```
