import logging

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="AI-powered business growth and publishing platform",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def startup_event():
    logger.info("Atlas AI backend started")


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "environment": settings.app_env,
        "status": "running",
        "version": "0.1.0",
    }
