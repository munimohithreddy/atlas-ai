# Atlas AI Sprints

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
