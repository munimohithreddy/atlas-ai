# Atlas AI Changelog

## Sprint 015: Campaign Task Execution

Added:

- Task execution fields on `CampaignTask` for started/completed timestamps, blocking reasons, completion notes, actual hours, assignment, and due dates.
- Deterministic task status transitions and dependency readiness services.
- Campaign progress derivation and next-ready task calculation.
- Task detail, task update, and task action endpoints under campaigns.
- Campaign task execution controls in the founder dashboard.
- Tests for readiness, transitions, dependency unlocks, progress, and restrictions.

Changed:

- Campaign task completion now supports fractional actual hours with numeric storage and validation.
- Campaign tasks are now the execution unit inside campaigns.
- Progress is derived from non-cancelled executable tasks.
- Campaign readiness remains distinct from publication.

## Sprint C3.1: Campaign Workspace Frontend Redesign

Added:

- Tabbed campaign workspace with Overview, Tasks, Assets, and Activity views.
- Human-readable status labels, next-action panels, grouped assets, and grouped production queue sections.
- Lightweight action guidance and contextual empty states for campaign work.

Changed:

- The frontend now reads campaign execution as a business workspace instead of a technical admin list.

## Sprint 014: Campaign Foundation

Added:

- Campaign, CampaignTask, and CampaignAsset models.
- Campaign repository and service layer.
- Campaign task generation, asset planning, and status transition services.
- `POST /api/v1/campaigns`, `GET /api/v1/campaigns`, `GET /api/v1/campaigns/{campaign_id}`, `PATCH /api/v1/campaigns/{campaign_id}`, `GET /api/v1/campaigns/{campaign_id}/tasks`, `GET /api/v1/campaigns/{campaign_id}/assets`, `POST /api/v1/campaigns/{campaign_id}/approve`, and `POST /api/v1/campaigns/{campaign_id}/status`.
- Founder dashboard campaign creation and campaign details display.
- Campaign migration and import coverage.
- Tests for creation, duplicate prevention, status transitions, task generation, asset planning, routing, and migration imports.

Changed:

- Campaigns are deterministic in v1 and only plan execution work.
- Tasks and assets are planning artifacts, not generated content or published output.
- Campaign approval is required before execution advances.

## Sprint 013: Business Planner Foundation

Added:

- Brand domain model, schemas, repository, routes, and migration.
- BusinessPlan domain model, schemas, repository, routes, and migration.
- Deterministic business-planning services for monetization, acquisition, revenue, and effort.
- `POST /api/v1/opportunities/{opportunity_id}/business-plan`.
- `GET /api/v1/brands`, `GET /api/v1/brands/{brand_id}`, `GET /api/v1/business-plans`, and `GET /api/v1/business-plans/{business_plan_id}`.
- Founder dashboard action for creating and displaying business plans.
- Tests for brand creation, duplicate slug rejection, business plan creation, recommendation services, missing opportunity handling, and route registration.

Changed:

- Business planning reuses existing Opportunity scores and evidence and stays deterministic in v1.
- External platforms are treated as acquisition channels, not monetization models.
- Documentation now records the Brand -> Opportunity -> BusinessPlan -> Campaign -> Assets -> Distribution -> Analytics -> Learning flow.

## Sprint 012: Founder Dashboard v0.1

Added:

- Minimal Next.js TypeScript frontend under `frontend/`.
- Founder dashboard page for portfolio evaluation.
- Frontend environment example with `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`.
- FastAPI CORS middleware for the local frontend origin.
- Backend CORS configuration test.
- Architecture documentation for the frontend and backend split.

Changed:

- README now includes backend and frontend setup, run, test, and verification commands.
- Git ignore rules now cover local Next.js build output.

## Sprint 011: Opportunity Portfolio Engine

Added:

- `POST /api/v1/opportunities/portfolio` for ranking multiple topics without persisting opportunities.
- `OpportunityPortfolioRequest`, `OpportunityPortfolioItemResponse`, and `OpportunityPortfolioResponse` schemas.
- Portfolio evaluation service under `backend/app/services/opportunities/portfolio.py`.
- Backend tests for portfolio endpoint behavior, ranking order, empty topic validation, duplicate topic handling, and route registration.

Changed:

- Opportunity routes now include portfolio evaluation before the `{opportunity_id}` detail route.

## Sprint 010: Evidence-Based Scoring Engine

Added:

- Opportunity evidence scoring service under `backend/app/services/opportunities/evidence_scoring.py`.
- Tests for single evidence scoring, confidence-weighted averaging, neutral defaults, affiliate mapping, and endpoint behavior.

Changed:

- Research evidence scoring now delegates to the opportunity evidence scoring service.
- Provider-backed opportunity evaluation now builds score inputs directly from evidence.
- `POST /api/v1/opportunities/evaluate-with-evidence` uses confidence-weighted evidence scores.

## Sprint 009: Affiliate Program Intelligence v1

Added:

- `AffiliateProgram` SQLAlchemy model.
- Alembic migration for `affiliate_programs`.
- Affiliate program schemas, repository, and API routes.
- Affiliate intelligence service for matching programs and estimating affiliate potential.
- Affiliate research provider for research preview.
- Tests for affiliate program creation, listing, scoring, and preview evidence.
- Database documentation.

Changed:

- Research preview now includes affiliate evidence when stored affiliate programs match the requested topic or niche.
- API router now includes affiliate program routes.

## Sprint 008: Research Provider Architecture

Added:

- Research provider package under `backend/app/services/research/providers/`.
- `ResearchProvider` protocol, `EvidenceSignal`, and `ResearchProviderResult`.
- Service-layer mock and manual evidence provider classes.
- `ResearchOrchestrator` for running multiple providers.
- `ResearchPreviewRequest` and research preview response schemas.
- `POST /api/v1/research/preview` endpoint.
- Tests for provider protocol conformance, mock/manual providers, orchestrator aggregation, and research preview.

Changed:

- Existing mock/manual provider import paths remain available as compatibility shims.
- API router now includes research routes alongside health and opportunities.

## Sprint 007: OpenAI Research Synthesizer v1

Added:

- `OPENAI_API_KEY` in `.env.example`.
- OpenAI Python dependency in backend requirements.
- OpenAI integration wrapper under `backend/app/integrations/openai/`.
- Opportunity analysis service with OpenAI-backed synthesis and deterministic fallback.
- AI analysis columns on `Opportunity`.
- Alembic migration for AI analysis fields.
- AI analysis fields on opportunity detail responses.
- Tests using a mocked OpenAI response.

Changed:

- `POST /api/v1/opportunities/evaluate-with-evidence` now stores AI/fallback analysis after calculating scores and evidence.

## Sprint 006: Real Research Provider v1

Added:

- Search integration package under `backend/app/integrations/search/`.
- `SearchResearchProvider` interface for search-style research providers.
- Manual evidence provider for API-submitted research evidence.
- Evidence scoring service that converts submitted evidence into opportunity score inputs.
- `OpportunityEvaluateWithEvidenceRequest` schema.
- `POST /api/v1/opportunities/evaluate-with-evidence` endpoint.
- Backend tests for manual evidence scoring, manual provider behavior, endpoint persistence, and router registration.

Changed:

- Research evaluation now supports both mock-generated evidence and manually submitted evidence.

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
