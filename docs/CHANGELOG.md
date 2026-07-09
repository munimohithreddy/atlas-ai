# Atlas AI Changelog

## Sprint 003: Foundation Hardening

Added:

- Backend dependency lock file based on the currently installed local backend environment.
- Safe `.env.example` for local development.
- Standard-library backend tests for opportunity scoring, health route imports, and API router registration.
- Sprint, changelog, and architecture decision documentation.

Changed:

- Alembic migration environment now establishes the backend import path before importing application models.
- Git ignore rules now cover `.venv-1/` and common local Python cache artifacts.
