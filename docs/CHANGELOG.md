# Atlas AI Changelog

## Sprint 005: Evidence and Decision Logging

Added:

- `OpportunityEvidence` SQLAlchemy model and relationship from `Opportunity`.
- Alembic migration for the `opportunity_evidence` table.
- Structured research evidence items from the mock research provider.
- Evidence persistence for `POST /api/v1/opportunities/evaluate`.
- `GET /api/v1/opportunities/{opportunity_id}` endpoint returning opportunity details plus evidence.
- Response and create schemas for opportunity evidence.
- Backend tests for evidence model creation, evaluate evidence persistence, and get-by-id evidence responses.

Changed:

- Mock research now returns a research result containing both score signals and evidence items.
- Opportunity repository creation can optionally persist evidence while preserving manual opportunity creation.

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
