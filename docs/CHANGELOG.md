# Atlas AI Changelog

## Sprint 004: Research Intelligence v1

Added:

- Research service package with a deterministic mock provider.
- Structured research signals for demand, competition, buyer intent, affiliate potential, Pinterest potential, and SEO potential.
- `OpportunityEvaluateRequest` schema for topic/niche-only evaluation.
- `POST /api/v1/opportunities/evaluate` endpoint.
- Backend tests for mock research, evaluate endpoint behavior, and router registration of the new route.
- API documentation for the opportunity endpoints.

Changed:

- Opportunity routes now support both manual score entry and mock research-backed evaluation.

## Sprint 003: Foundation Hardening

Added:

- Backend dependency lock file based on the currently installed local backend environment.
- Safe `.env.example` for local development.
- Standard-library backend tests for opportunity scoring, health route imports, and API router registration.
- Sprint, changelog, and architecture decision documentation.

Changed:

- Alembic migration environment now establishes the backend import path before importing application models.
- Git ignore rules now cover `.venv-1/` and common local Python cache artifacts.
