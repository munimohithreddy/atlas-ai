from fastapi import APIRouter

from app.database.redis import check_redis_connection
from app.database.session import check_database_connection

router = APIRouter()


@router.get("/health")
def health():
    database_ok = check_database_connection()
    redis_ok = check_redis_connection()

    app_ok = database_ok and redis_ok

    return {
        "application": "healthy" if app_ok else "degraded",
        "database": "healthy" if database_ok else "unhealthy",
        "redis": "healthy" if redis_ok else "unhealthy",
        "version": "0.1.0",
    }
