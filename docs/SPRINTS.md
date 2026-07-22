# Atlas AI Sprints

## Sprint 015: Campaign Task Execution

Goal: allow Atlas founders to execute a campaign through ordered, dependency-aware tasks while measuring progress and identifying the next actionable work.

Scope:

- Add task execution fields to `CampaignTask`.
- Add deterministic task status transitions.
- Add dependency validation and downstream readiness recalculation.
- Add campaign progress derivation and next-ready task calculation.
- Extend campaign task endpoints for detail, update, and actions.
- Extend the founder dashboard with task execution controls and progress display.
- Add tests for readiness, transitions, dependency unlocks, progress, and restrictions.
- Support fractional actual hours on task completion with numeric persistence.

## Sprint C3.1: Campaign Workspace Frontend Redesign

Goal: make campaign execution understandable to non-technical users through guided tabs, business-readable labels, and a clearer asset production queue.

Scope:

- Redesign the campaign workspace into Overview, Tasks, Assets, and Activity tabs.
- Add a prominent next-action panel and clearer campaign progress summaries.
- Group assets and queue items by business stage with one primary action per item.
- Translate technical statuses into business-friendly labels and guidance.

Out of scope:

- Content generation.
- Asset production.
- External publishing.
- Scheduling.
- Background workers.
- Third-party integrations.

## Sprint C3.5: Professional SaaS Workflow UI

Goal: turn the founder dashboard into a professional operating workspace for moving from opportunity selection through business planning, campaign execution, task readiness, asset production, and publishing readiness.

Scope:

- Add a SaaS-style application shell with sidebar navigation, breadcrumbs, mobile navigation, and development environment indicator.
- Add a dashboard summary with opportunity, plan, campaign, task, and asset counts.
- Add workflow guidance, next-action messaging, attention items, and recent activity.
- Expand opportunity and business-plan presentation with clear strategy, audience, monetization, acquisition, content, launch, and campaign actions.
- Keep the campaign workspace focused with Overview, Tasks, Assets, and Activity tabs.
- Group campaign assets by production stage while keeping the global production queue grouped by operational urgency.
- Improve empty, loading, success, and error states without adding new backend behavior.

Out of scope:

- Authentication.
- Billing.
- Content generation.
- Publishing integrations.
- Scheduling.
- Background workers.
- New backend APIs.

## Sprint C3.6: Guided SaaS Product Experience

Goal: make Atlas understandable and operable for a first-time user without external explanation while preserving the business workflow from Opportunity to Ready to Publish.

Scope:

- Replace technical dashboard language with plain business language.
- Add a first-run onboarding experience for an empty database.
- Remove global Tasks and Assets navigation; keep them scoped inside the Campaign Workspace.
- Add visible Opportunity -> Business Plan -> Campaign relationships.
- Add human-readable enum formatting and generated campaign names.
- Improve task and asset cards with descriptions, dependencies, valid actions, and lifecycle guidance.
- Improve the global Production Queue with dropdown filters, clear filters, loading states, and campaign context links.
- Fix task dependency readiness so only completed dependencies unlock downstream tasks.
- Add a plain-language product glossary and manual clean-database acceptance flow.

Out of scope:

- AI content generation.
- Website generation.
- Publishing integrations.
- Authentication.
- Billing.
- Analytics dashboards.
- Revenue integrations.
- New campaign lifecycle capabilities.

## Sprint 014: Campaign Foundation

Goal: convert an approved BusinessPlan into a launch-ready Campaign with deterministic tasks, planned assets, revenue goals, and measurable campaign status.

Scope:

- Add Campaign, CampaignTask, and CampaignAsset models.
- Add deterministic campaign services for creation, task generation, asset planning, and status transitions.
- Add campaign CRUD, task listing, asset listing, approval, and status endpoints.
- Extend the founder dashboard with campaign creation and campaign details display.
- Add tests for campaign creation, duplicate prevention, status transitions, tasks, assets, router registration, and migration imports.
- Update product, API, database, changelog, decision, and architecture documentation.

Out of scope:

- Content generation.
- OpenAI generation.
- Publishing integrations.
- Scheduling.
- Analytics ingestion.
- Authentication.
- Billing.

## Sprint 013: Business Planner Foundation

Goal: turn a ranked opportunity into an explainable initial business plan that Atlas can later execute through campaigns, assets, distribution, analytics, and learning.

Scope:

- Add Brand and BusinessPlan domain models.
- Add deterministic business planning services for monetization, acquisition, revenue, and effort.
- Add business plan creation and retrieval endpoints.
- Extend the founder dashboard with a Create Business Plan action and plan summary display.
- Update product, API, database, changelog, and decision documentation.
- Add tests for brand creation, duplicate slug rejection, business plan creation, recommendation services, missing opportunity handling, and route registration.

Out of scope:

- Authentication.
- Payments.
- Charts.
- Scheduling.
- Publishing.
- Website generation.

## Sprint 012: Founder Dashboard v0.1

Goal: give the founder a usable interface for evaluating and ranking business opportunities without using Swagger or raw JSON.

Scope:

- Add a minimal Next.js, TypeScript, App Router frontend under `frontend/`.
- Add a founder dashboard page with Atlas AI heading, niche input, multiline topics input, submit button, loading state, and error state.
- Call `POST /api/v1/opportunities/portfolio` through `NEXT_PUBLIC_API_BASE_URL`.
- Display ranked portfolio results with recommendation badges and all returned score fields.
- Add frontend validation for optional niche, at least one non-empty topic, trimming, and duplicate topic removal.
- Add local frontend environment example with `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`.
- Add FastAPI CORS middleware allowing `http://localhost:3000`.
- Update README and architecture documentation for the new frontend surface.

Out of scope:

- Authentication.
- Billing.
- Charts.
- Additional UI frameworks.

## Sprint 011: Opportunity Portfolio Engine

Goal: evaluate multiple opportunity topics in one request and rank them by Business Opportunity Score.

Scope:

- Add `POST /api/v1/opportunities/portfolio`.
- Add request and response schemas for portfolio evaluation.
- Use the existing `ResearchOrchestrator` to collect evidence for each topic.
- Use the existing evidence-based scoring service to calculate normalized score inputs.
- Use the existing opportunity score and recommendation service to calculate `business_score` and recommendation.
- Return ranked, non-persisted portfolio results sorted by highest `business_score`.
- Calculate a portfolio confidence value from collected evidence confidence.
- Validate empty topic lists and de-duplicate submitted topics case-insensitively before evaluation.
- Add tests for the endpoint, ranking order, empty topic validation, duplicate topic handling, and route registration.

Out of scope:

- Persisting portfolio results as `Opportunity` rows.
- External APIs.
- Scraping.

## Sprint 010: Evidence-Based Scoring Engine

Goal: improve opportunity scoring so Atlas aggregates evidence by signal type using confidence-weighted scoring.

Scope:

- Add `backend/app/services/opportunities/evidence_scoring.py`.
- Calculate normalized opportunity score inputs from evidence items.
- Use confidence-weighted averages for multiple evidence items with the same signal type.
- Map `affiliate_potential` evidence to `affiliate_score`.
- Use a documented neutral default of `50` for missing required scores.
- Update provider-backed evaluation flows to use the opportunity evidence scoring service.
- Keep manual `POST /api/v1/opportunities` working.
- Add tests for single evidence, weighted evidence, missing defaults, affiliate mapping, and endpoint usage.

Out of scope:

- External APIs.
- Scraping.

## Sprint 009: Affiliate Program Intelligence v1

Goal: add structured affiliate intelligence so Atlas can evaluate monetization potential from stored affiliate programs.

Scope:

- Add `AffiliateProgram` model and migration.
- Add schemas, repository, and API routes for affiliate programs.
- Add `POST /api/v1/affiliate-programs`.
- Add `GET /api/v1/affiliate-programs`.
- Add `GET /api/v1/affiliate-programs/{id}`.
- Add affiliate potential estimation from stored programs.
- Include affiliate evidence in research preview when matching programs exist.
- Add tests for affiliate program creation/listing, affiliate potential estimation, and affiliate evidence in preview.
- Update API, sprint, changelog, decision, and database documentation.

Out of scope:

- Scraping.
- External affiliate APIs.

## Sprint 008: Research Provider Architecture

Goal: create a clean provider architecture for future evidence collection without adding real external APIs yet.

Scope:

- Add `backend/app/services/research/providers/`.
- Define a `ResearchProvider` protocol and `EvidenceSignal` data structure.
- Move mock and manual evidence behavior into provider classes.
- Add `ResearchOrchestrator` to run one or more providers for a topic and niche.
- Keep existing opportunity evaluation endpoints working.
- Add `POST /api/v1/research/preview` to preview provider evidence without creating an opportunity.
- Add tests for provider protocol conformance, mock provider, manual provider, orchestrator aggregation, and research preview.
- Update API, sprint, changelog, and decision documentation.

Out of scope:

- Real external APIs.
- Scraping.

## Sprint 007: OpenAI Research Synthesizer v1

Goal: synthesize submitted evidence into a clearer opportunity analysis while keeping deterministic fallback behavior.

Scope:

- Add optional OpenAI configuration through `OPENAI_API_KEY`.
- Add the OpenAI Python dependency.
- Add `backend/app/integrations/openai/` with an OpenAI client wrapper.
- Add a research synthesis service that accepts topic, niche, evidence, and calculated scores.
- Store AI analysis fields on `Opportunity`.
- Add an Alembic migration for AI analysis columns.
- Include AI analysis fields in `GET /api/v1/opportunities/{opportunity_id}`.
- Keep the system working without `OPENAI_API_KEY` by using deterministic fallback analysis.
- Add tests with a mocked OpenAI response.

Out of scope:

- Scraping.
- External search APIs.
- OpenAI-powered evidence gathering.

## Sprint 006: Real Research Provider v1

Goal: add the first real research-provider boundary while keeping the mock provider available for tests and local development.

Scope:

- Add `backend/app/integrations/search/` for search-style research provider abstractions.
- Add a `SearchResearchProvider` interface.
- Add a manual evidence provider that accepts researched evidence submitted through the API.
- Add evidence scoring that converts submitted evidence into opportunity scores.
- Add `POST /api/v1/opportunities/evaluate-with-evidence`.
- Store the resulting opportunity and submitted evidence rows.
- Keep `POST /api/v1/opportunities/evaluate` working with the mock provider.
- Add tests for manual evidence scoring, the manual provider, endpoint persistence, and route registration.
- Update API, sprint, changelog, and decision documentation.

Out of scope:

- OpenAI integrations.
- Scraping.
- Google Trends, Reddit, Pinterest, or affiliate network integrations.

## Sprint 005: Evidence and Decision Logging

Goal: store the evidence and research signals used to score every evaluated opportunity.

Scope:

- Add `OpportunityEvidence` as a first-class SQLAlchemy model.
- Add a database migration for the `opportunity_evidence` table.
- Relate opportunities to evidence rows.
- Update mock research to return structured evidence items alongside score signals.
- Store evidence rows when `POST /api/v1/opportunities/evaluate` creates an opportunity.
- Add `GET /api/v1/opportunities/{opportunity_id}` to return an opportunity with evidence.
- Add tests for evidence model creation, evaluate evidence persistence, and get-by-id evidence responses.
- Update API, sprint, changelog, and decision documentation.

Out of scope:

- External API calls.
- OpenAI, Google Trends, Reddit, Pinterest, or affiliate network integrations.

## Sprint 004: Research Intelligence v1

Goal: let Atlas evaluate an opportunity from a topic and optional niche without requiring manual score entry.

Scope:

- Add a research service layer under `backend/app/services/research/`.
- Add a deterministic mock research provider with structured demand, competition, buyer intent, affiliate, Pinterest, and SEO signals.
- Add `POST /api/v1/opportunities/evaluate` for topic/niche-only opportunity evaluation.
- Reuse the existing opportunity repository and response model so manual opportunity creation keeps working.
- Add tests for the mock provider, evaluate endpoint, and existing scoring behavior.
- Document the new API and Sprint 004 decisions.

Out of scope:

- OpenAI integrations.
- Google Trends, Reddit, Pinterest, or affiliate network integrations.
- AI agents.

## Sprint 003: Foundation Hardening

Goal: make the Atlas Core backend reproducible, testable, and easier to run before adding new product surface.

Scope:

- Capture backend dependencies in `backend/requirements.txt`.
- Add safe local environment documentation through `.env.example`.
- Expand local Python and virtual environment ignores.
- Fix Alembic imports so migrations can run from the repository root or backend folder.
- Add focused backend tests for opportunity scoring, health imports, and API router registration.
- Start sprint, changelog, and decision documentation under `docs/`.

Out of scope:

- AI agents.
- Product workflow refactors.
- New database models or API resources.
