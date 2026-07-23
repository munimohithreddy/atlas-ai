# Atlas AI Decisions

## Sprint C3.6: Guided SaaS Product Experience

### Tasks and Assets are campaign-scoped navigation

Tasks and Assets are no longer global sidebar destinations because they only have useful meaning within a selected campaign.

### The primary dashboard action creates a stored Opportunity

The old portfolio evaluation flow remains available as a secondary comparison action, but the main path now creates a persisted Opportunity so onboarding can progress through the real Atlas workflow.

### Cancelled task dependencies do not unlock downstream tasks

Only completed dependencies satisfy downstream readiness. Cancelling a dependency leaves dependent pending work waiting instead of silently creating an impossible launch path.

### Activity is labelled as updates until event storage exists

The frontend summarizes real campaign state as Recent Updates instead of inventing an activity history.

## Sprint C3.5: Professional SaaS Workflow UI

### The frontend remains a single founder workspace route

Sprint C3.5 improves the operating model inside the existing dashboard route instead of adding premature route structure. The app shell, sidebar sections, and mobile navigation organize the workflow while preserving the existing API integration surface.

### Dashboard sections follow the business workflow

The primary navigation mirrors how a founder works: Dashboard, Opportunities, Business Plans, Campaigns, Tasks, Assets, Production Queue, Documentation, and Settings.

### Asset stages differ from queue urgency groups

Campaign asset views show detailed production stages. The global production queue keeps five operational groups so the queue remains focused on what needs action next.

## Sprint 015: Campaign Task Execution

### Campaign Tasks are the unit of execution

Execution happens by moving tasks through deterministic states rather than by changing campaign state directly.

### Tasks may not execute before Campaign approval

Planning can exist before approval, but task start is blocked until the campaign enters an approved execution state.

### Dependencies are deterministic and campaign-scoped

Tasks only unlock through their own campaign dependencies, and cross-campaign dependencies are rejected.

### Completing tasks unlocks downstream tasks

When a task finishes, dependent downstream tasks are recalculated and can move to ready if their dependencies are satisfied.

### Campaign progress is derived from non-cancelled executable tasks

The denominator excludes cancelled tasks and avoids division by zero when no executable work exists.

### Task completion does not publish assets or the Campaign

A completed task can advance campaign readiness, but it does not trigger publication.

### Campaign readiness is distinct from publication

The ready state means a campaign can execute further work or await publication; it does not mean the campaign has gone live.

## Sprint 014: Campaign Foundation

### Nothing may be generated or published unless it belongs to a campaign

Campaigns become the execution boundary. Content, assets, and distribution work are only planned through a campaign record.

### Campaign creation is deterministic in v1

Campaign names, slugs, tasks, assets, revenue targets, and build estimates are derived from the approved BusinessPlan without calling OpenAI.

### Campaign approval is required before execution

Campaigns start in planning and must be explicitly approved before they can move into execution-oriented states.

### Tasks and assets are plans only in this milestone

Sprint 014 creates execution plans, not generated content or publishing actions.

### Monetization and acquisition remain separate concepts

Campaign planning reuses the BusinessPlan separation between monetization strategy and acquisition strategy.

### External platforms are acquisition and distribution channels

Campaign assets and tasks may target external channels, but those channels remain distribution surfaces rather than the source of the business model.

## Sprint 013: Business Planner Foundation

### Atlas creates brands, not one website per keyword

The first durable planning layer introduces brands as the unit of ownership. Opportunities feed a brand-specific business plan instead of spawning isolated keyword sites.

### Monetization and acquisition are separate decisions

The business planner first chooses how an opportunity makes money, then chooses how it will acquire traffic. This keeps strategy clearer and makes recommendations easier to explain.

### Business planning is deterministic in v1

Sprint 013 keeps planning rules fully deterministic. Existing opportunity scores and evidence provide the inputs, but the new planner does not call OpenAI.

### External platforms are acquisition channels

Pinterest, YouTube, email, Reddit, LinkedIn, Instagram, and direct outreach are treated as acquisition channels. Monetization models remain separate from distribution.

### Human approval is required before campaign launch

Business plans can be drafted and reviewed in Atlas, but launching campaigns remains a human approval step for now.

## Sprint 012: Founder Dashboard v0.1

### Start with one focused dashboard

The first frontend surface is a single founder dashboard for portfolio evaluation. This keeps the product usable while avoiding premature navigation, authentication, billing, charts, or workflow expansion.

### Keep frontend logic client-side and narrow

The dashboard validates and normalizes form input in the browser, then calls the existing portfolio endpoint. Ranking and scoring remain backend responsibilities.

### Use plain CSS

Sprint 012 uses simple project-local CSS instead of adding a UI framework. This keeps dependencies low and leaves room for a more deliberate design system later.

### Configure local CORS explicitly

FastAPI allows `http://localhost:3000` so the local Next.js app can call the backend during development. Broader CORS policy can be introduced later through configuration when deployment targets are known.

## Sprint 011: Opportunity Portfolio Engine

### Keep portfolio evaluation non-persistent

Portfolio ranking is a comparison workflow, not a decision record. The endpoint returns ranked results without creating `Opportunity` rows so users can explore topic sets without polluting stored opportunities.

### Compose existing research and scoring services

The portfolio service uses `ResearchOrchestrator`, `calculate_scores_from_evidence`, `calculate_opportunity_score`, and `make_recommendation`. This keeps scoring behavior consistent with existing opportunity evaluation and avoids duplicate scoring logic.

### Rank by Business Opportunity Score

Portfolio results expose the calculated opportunity score as `business_score` and sort descending. The response includes rank numbers after sorting so clients can display a stable ordered portfolio.

### De-duplicate submitted topics

Submitted topics are trimmed and de-duplicated case-insensitively before evaluation. This avoids repeated provider work and keeps portfolio results focused on unique ideas.

### Use evidence confidence for portfolio confidence

Portfolio confidence is the rounded average `confidence_score` across collected evidence. If a topic has no evidence, confidence is `0`.

## Sprint 010: Evidence-Based Scoring Engine

### Make opportunity evidence scoring canonical

Evidence aggregation determines opportunity score inputs, so the canonical implementation lives under `services/opportunities/`. Research services can collect evidence, but opportunity services own scoring decisions.

### Use confidence-weighted averages per signal type

When multiple evidence items support the same signal, Atlas weights each value by `confidence_score`. Higher-confidence evidence has more influence while still allowing weaker evidence to contribute.

### Default missing scores to neutral 50

Missing evidence should not crash evaluation or imply a zero score. Atlas uses `50` as a neutral midpoint for required score fields when no matching evidence exists.

### Preserve manual score entry

Manual `POST /api/v1/opportunities` still accepts explicit score fields. Evidence-based scoring applies to provider-backed evaluation flows.

## Sprint 009: Affiliate Program Intelligence v1

### Store affiliate programs before integrating networks

Atlas can reason about monetization potential from curated affiliate program records before adding external affiliate APIs. This keeps the first affiliate intelligence layer deterministic and testable.

### Keep affiliate matching simple and transparent

Sprint 009 matches stored programs against topic and niche using program name, category, network, and notes. The logic is intentionally simple so users can understand why affiliate evidence appeared.

### Represent affiliate intelligence as research evidence

Matching affiliate programs produce an `affiliate_potential` evidence signal in research preview. This lets affiliate intelligence reuse the existing provider and evidence architecture.

### Do not scrape or call affiliate networks yet

Affiliate programs are entered through Atlas APIs. External affiliate networks can be added later behind provider interfaces.

## Sprint 008: Research Provider Architecture

### Move provider contracts into the research service layer

Provider orchestration is business behavior, so the durable provider protocol lives under `services/research/providers/`. Integration packages can still adapt external systems later, but scoring and orchestration remain service-owned.

### Keep compatibility shims for existing provider imports

Existing mock and manual provider import paths continue to work. This keeps the sprint targeted and avoids unrelated endpoint or test churn.

### Add preview before persistence

`POST /api/v1/research/preview` lets Atlas inspect provider evidence before creating an opportunity. This makes future real providers easier to validate without polluting opportunity history.

### Use mock provider as the default orchestrator provider

Until real external providers exist, the orchestrator defaults to the mock provider. That keeps local development deterministic while exercising the same architecture future providers will use.

## Sprint 007: OpenAI Research Synthesizer v1

### Use OpenAI only for synthesis, not research collection

Sprint 007 uses OpenAI to turn submitted evidence and calculated scores into a clearer analysis. It does not scrape websites, call external search APIs, or gather evidence automatically.

### Keep OpenAI optional at runtime

If `OPENAI_API_KEY` is missing, the app returns deterministic fallback analysis instead of crashing. This keeps local development, tests, and non-OpenAI deployments working.

### Store analysis on the opportunity

The synthesized analysis is part of the decision record for an opportunity, so it lives on the `Opportunity` row and is returned by the detail endpoint with evidence.

### Treat invalid AI output as unavailable

If the OpenAI response is missing, non-JSON, or does not include the expected fields, Atlas falls back to deterministic analysis rather than returning partial or malformed data.

## Sprint 006: Real Research Provider v1

### Use manual evidence as the first non-mock research provider

Atlas needs a provider boundary before external integrations. Manual evidence lets users submit researched facts from any source while Atlas handles scoring, persistence, and decision logging.

### Keep search integrations abstract and non-scraping

The search provider interface models a future web-search-style research source, but Sprint 006 does not scrape pages or call third-party APIs. This keeps the architecture ready without adding operational or compliance risk.

### Score submitted evidence in the service layer

The manual provider accepts evidence, while `services/research/evidence_scoring.py` converts it into opportunity score inputs. This follows the project rule that business logic belongs in services.

### Default missing signals to neutral scores

Submitted evidence may cover only some signal types. Missing signals default to `50`, a neutral midpoint, so partial evidence can still produce an opportunity while making gaps visible in stored evidence.

## Sprint 005: Evidence and Decision Logging

### Store evidence separately from opportunity scores

Opportunity scores are the decision output. Evidence rows are the supporting inputs. Keeping them separate lets Atlas show why an opportunity was scored without changing the existing opportunity table each time research sources evolve.

### Keep evaluate responses backward compatible

`POST /api/v1/opportunities/evaluate` still returns `OpportunityResponse`. Evidence is available through the detail endpoint so existing create/evaluate clients keep the same response shape.

### Persist mock evidence now, external evidence later

The mock provider now produces evidence items with source, signal type, value, summary, and confidence. This establishes the storage contract without calling external APIs yet.

## Sprint 004: Research Intelligence v1

### Use a deterministic mock research provider first

Atlas needs a stable research contract before external integrations are introduced. The mock provider returns structured signals without calling OpenAI, Google Trends, Reddit, Pinterest, or affiliate networks.

### Convert research signals into the existing opportunity creation schema

The evaluate endpoint builds an `OpportunityCreate` payload from research signals and then reuses the existing repository path. This keeps scoring, recommendation, persistence, and response behavior consistent with manual opportunity creation.

### Keep provider output simple and score-shaped

The first provider returns integer signals on the same `0..100` scale used by opportunity scoring. This makes the provider easy to test and easy to replace later with real research integrations.

## Sprint 003: Foundation Hardening

### Use `backend/requirements.txt` for the current backend dependency baseline

Atlas does not yet have a package manifest. A pinned requirements file gives the backend a reproducible installation path without introducing a larger packaging refactor.

### Use standard-library tests for the first backend test suite

The current installed backend environment does not include a test runner dependency. The initial tests use `unittest` so they can run immediately from the existing environment.

### Keep Alembic compatible with root and backend execution

Migration commands should work whether an engineer runs Alembic from the repository root with `-c backend/alembic.ini` or from inside `backend/`. The migration environment now adds the backend directory to `sys.path` before importing application modules.

### Do not add agents during foundation hardening

Sprint 003 focuses on reproducibility, migrations, and tests. AI agents remain intentionally out of scope until the backend foundation is stable.
