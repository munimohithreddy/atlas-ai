from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.repositories.campaign_asset_repository import list_campaign_assets
from app.repositories.campaign_repository import get_campaign, list_campaigns, update_campaign
from app.repositories.campaign_task_repository import list_campaign_tasks
from app.schemas.campaign import (
    CampaignAssetResponse,
    CampaignCreate,
    CampaignDetailResponse,
    CampaignResponse,
    CampaignTaskResponse,
    CampaignUpdate,
)
from app.services.campaigns.service import CampaignService
from app.services.campaigns.status import CampaignStatusService

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("", response_model=CampaignResponse)
def create(payload: CampaignCreate, db: Session = Depends(get_db)):
    try:
        return CampaignService().create_campaign(
            db=db,
            business_plan_id=payload.business_plan_id,
            goal=payload.goal,
            priority=payload.priority,
            launch_target_date=payload.launch_target_date,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("", response_model=list[CampaignResponse])
def list_all(offset: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return list_campaigns(db, offset=offset, limit=limit)


@router.get("/{campaign_id}", response_model=CampaignDetailResponse)
def get_by_id(campaign_id: int, db: Session = Depends(get_db)):
    campaign = get_campaign(db, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign.tasks = list_campaign_tasks(db, campaign.id)
    campaign.assets = list_campaign_assets(db, campaign.id)
    return campaign


@router.patch("/{campaign_id}", response_model=CampaignResponse)
def patch_campaign(campaign_id: int, payload: CampaignUpdate, db: Session = Depends(get_db)):
    campaign = get_campaign(db, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(campaign, field, value)
    return update_campaign(db, campaign)


@router.get("/{campaign_id}/tasks", response_model=list[CampaignTaskResponse])
def get_tasks(campaign_id: int, db: Session = Depends(get_db)):
    return list_campaign_tasks(db, campaign_id)


@router.get("/{campaign_id}/assets", response_model=list[CampaignAssetResponse])
def get_assets(campaign_id: int, db: Session = Depends(get_db)):
    return list_campaign_assets(db, campaign_id)


@router.post("/{campaign_id}/approve", response_model=CampaignResponse)
def approve(campaign_id: int, db: Session = Depends(get_db)):
    campaign = get_campaign(db, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    try:
        CampaignStatusService().transition(campaign, "approved")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return update_campaign(db, campaign)


@router.post("/{campaign_id}/status", response_model=CampaignResponse)
def change_status(campaign_id: int, status: str, db: Session = Depends(get_db)):
    campaign = get_campaign(db, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    try:
        CampaignStatusService().transition(campaign, status)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return update_campaign(db, campaign)
