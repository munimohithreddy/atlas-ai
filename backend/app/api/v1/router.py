from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.affiliate_programs import router as affiliate_programs_router
from app.api.v1.campaigns import router as campaigns_router
from app.api.v1.brands import router as brands_router
from app.api.v1.business_plans import router as business_plans_router
from app.api.v1.health import router as health_router
from app.api.v1.opportunities.routes import router as opportunities_router
from app.api.v1.research import router as research_router
from app.database.deps import get_db
from app.repositories.campaign_asset_repository import list_asset_queue
from app.schemas.campaign import CampaignAssetResponse

api_router = APIRouter()


@api_router.get("/asset-production-queue", response_model=list[CampaignAssetResponse])
def asset_production_queue(
    campaign_id: int | None = None,
    status: str | None = None,
    channel: str | None = None,
    asset_type: str | None = None,
    assigned_to: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
):
    return list_asset_queue(
        db,
        campaign_id=campaign_id,
        status=status,
        channel=channel,
        asset_type=asset_type,
        assigned_to=assigned_to,
        priority=priority,
    )

api_router.include_router(affiliate_programs_router)
api_router.include_router(campaigns_router)
api_router.include_router(brands_router)
api_router.include_router(business_plans_router)
api_router.include_router(health_router, tags=['health'])
api_router.include_router(opportunities_router)
api_router.include_router(research_router)
