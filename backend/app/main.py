from fastapi import FastAPI

from app.core.config import settings
from app.database.session import check_database_connection

app = FastAPI(
    title=settings.app_name,
    description="AI-powered publishing and affiliate marketing platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "environment": settings.app_env,
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    database_ok = check_database_connection()

    return {
        "status": "healthy" if database_ok else "degraded",
        "database": "connected" if database_ok else "disconnected",
    }
