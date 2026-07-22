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

The frontend is a Next.js App Router application under `frontend/`.

The dashboard page is the founder operating workspace. It includes:

- a SaaS-style app shell with sidebar navigation, breadcrumbs, mobile section navigation, and development environment indicator,
- first-run onboarding when no opportunities, business plans, or campaigns exist,
- optional niche and business-idea inputs for opportunity creation,
- client-side topic trimming, de-duplication, and validation,
- persisted opportunity creation through `POST /api/v1/opportunities/evaluate`,
- portfolio results from `POST /api/v1/opportunities/portfolio`,
- business-plan creation and strategy review,
- campaign selection and a focused campaign workspace,
- task readiness and asset production rollups,
- the global asset production queue from `GET /api/v1/asset-production-queue`.

The campaign workspace presents campaign execution as a guided business flow with Overview, Tasks, Assets, and Activity tabs. Tasks and Assets are intentionally scoped to the selected campaign and are not global sidebar destinations. Campaign assets are grouped by detailed production stage, while the global production queue remains grouped by operational urgency. Statuses are translated into business-readable labels so the interface reads like an operating workspace instead of an admin console.

Workflow relationship display is handled in the frontend from currently available API fields:

- Opportunity cards show linked business plans and campaigns when loaded.
- Business Plan cards show their linked opportunity and campaigns.
- Campaign cards show linked opportunity and business plan identifiers or loaded names.

Critical lifecycle decisions remain backend-owned. For campaign tasks, only completed dependencies unlock downstream pending tasks; blocked or cancelled dependencies do not unlock dependents.

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
