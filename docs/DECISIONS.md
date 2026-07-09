# Atlas AI Decisions

## Sprint 003: Foundation Hardening

### Use `backend/requirements.txt` for the current backend dependency baseline

Atlas does not yet have a package manifest. A pinned requirements file gives the backend a reproducible installation path without introducing a larger packaging refactor.

### Use standard-library tests for the first backend test suite

The current installed backend environment does not include a test runner dependency. The initial tests use `unittest` so they can run immediately from the existing environment.

### Keep Alembic compatible with root and backend execution

Migration commands should work whether an engineer runs Alembic from the repository root with `-c backend/alembic.ini` or from inside `backend/`. The migration environment now adds the backend directory to `sys.path` before importing application modules.

### Do not add agents during foundation hardening

Sprint 003 focuses on reproducibility, migrations, and tests. AI agents remain intentionally out of scope until the backend foundation is stable.
