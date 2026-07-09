# Atlas AI Decisions

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
