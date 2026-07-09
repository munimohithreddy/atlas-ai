# Atlas AI Sprints

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
