# Atlas AI Architecture

Atlas AI currently has two runtime surfaces:

- `backend/`: FastAPI API server for research, opportunity scoring, evidence logging, affiliate intelligence, and portfolio ranking.
- `frontend/`: Next.js founder dashboard for evaluating and ranking business opportunities through the backend API.

## Backend

The backend exposes versioned APIs under `/api/v1`.

Key layers:

- `app/api`: HTTP routes only.
- `app/schemas`: Pydantic request and response contracts.
- `app/services`: business logic for scoring, portfolio evaluation, research orchestration, and AI synthesis.
- `app/repositories`: database persistence.
- `app/models`: SQLAlchemy models.
- `app/integrations`: third-party integration boundaries.

Sprint 012 adds CORS middleware in `app/main.py` for the local frontend origin `http://localhost:3000`.

## Frontend

The frontend is a minimal Next.js App Router application under `frontend/`.

The dashboard page:

- accepts an optional niche,
- accepts one topic per line,
- trims input,
- removes duplicate topics,
- requires at least one non-empty topic,
- calls `POST /api/v1/opportunities/portfolio`,
- displays ranked opportunity results.

The API base URL is configured through:

```text
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## Data Flow

1. The founder enters a niche and candidate topics in the dashboard.
2. The frontend normalizes topics and sends them to the portfolio endpoint.
3. The backend research orchestrator collects evidence for each topic.
4. The backend evidence scoring service converts evidence into normalized scores.
5. The backend opportunity scoring service calculates `business_score` and recommendation.
6. The frontend renders ranked results without persisting new opportunities.
