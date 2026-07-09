# Atlas AI Sprints

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
