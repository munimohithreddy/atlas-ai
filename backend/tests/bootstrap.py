import os
import sys
from pathlib import Path


def configure_test_environment() -> None:
    backend_dir = Path(__file__).resolve().parents[1]
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    os.environ.setdefault("APP_NAME", "Atlas AI")
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("APP_DEBUG", "false")
    os.environ.setdefault("POSTGRES_USER", "atlas")
    os.environ.setdefault("POSTGRES_PASSWORD", "atlas_password")
    os.environ.setdefault("POSTGRES_DB", "atlas_ai")
    os.environ.setdefault("POSTGRES_HOST", "localhost")
    os.environ.setdefault("POSTGRES_PORT", "5432")
    os.environ.setdefault("REDIS_HOST", "localhost")
    os.environ.setdefault("REDIS_PORT", "6379")
