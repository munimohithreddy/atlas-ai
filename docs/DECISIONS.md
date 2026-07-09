# Atlas AI Decisions

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
