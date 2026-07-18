from fastapi import APIRouter

from app.api.v1.affiliate_programs import router as affiliate_programs_router
from app.api.v1.campaigns import router as campaigns_router
from app.api.v1.brands import router as brands_router
from app.api.v1.business_plans import router as business_plans_router
from app.api.v1.health import router as health_router
from app.api.v1.opportunities.routes import router as opportunities_router
from app.api.v1.research import router as research_router

api_router = APIRouter()
api_router.include_router(affiliate_programs_router)
api_router.include_router(campaigns_router)
api_router.include_router(brands_router)
api_router.include_router(business_plans_router)
api_router.include_router(health_router, tags=['health'])
api_router.include_router(opportunities_router)
api_router.include_router(research_router)
