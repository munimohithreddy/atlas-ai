from fastapi import APIRouter, Depends, HTTPException, Query
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
    CampaignTaskBlockRequest,
    CampaignTaskCompleteRequest,
    CampaignTaskDetailResponse,
    CampaignTaskReopenRequest,
    CampaignTaskResponse,
    CampaignTaskStatusRequest,
    CampaignTaskUpdate,
    CampaignUpdate,
)
from app.services.campaigns.progress import CampaignProgressService
from app.services.campaigns.service import CampaignService
from app.services.campaigns.status import CampaignStatusService
from app.services.campaigns.task_service import CampaignTaskService

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


def _campaign_or_404(db: Session, campaign_id: int):
    campaign = get_campaign(db, campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


def _task_or_404(db: Session, campaign_id: int, task_id: int):
    task = CampaignTaskService().get_task(db, campaign_id, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=CampaignResponse)
def create(payload: CampaignCreate, db: Session = Depends(get_db)):
    try:
        campaign = CampaignService().create_campaign(
            db=db,
            business_plan_id=payload.business_plan_id,
            goal=payload.goal,
            priority=payload.priority,
            launch_target_date=payload.launch_target_date,
        )
        campaign.progress = CampaignProgressService().build_progress(db, campaign)
        return campaign
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Business plan not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail="Campaign already exists for this business plan") from exc


@router.get("", response_model=list[CampaignResponse])
def list_all(offset: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    campaigns = list_campaigns(db, offset=offset, limit=limit)
    for campaign in campaigns:
        campaign.progress = CampaignProgressService().build_progress(db, campaign)
    return campaigns


@router.get("/{campaign_id}", response_model=CampaignDetailResponse)
def get_by_id(campaign_id: int, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    campaign.tasks = list_campaign_tasks(db, campaign.id)
    campaign.assets = list_campaign_assets(db, campaign.id)
    campaign.progress = CampaignProgressService().build_progress(db, campaign)
    return campaign


@router.patch("/{campaign_id}", response_model=CampaignResponse)
def patch_campaign(campaign_id: int, payload: CampaignUpdate, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(campaign, field, value)
    campaign.progress = CampaignProgressService().build_progress(db, campaign)
    return update_campaign(db, campaign)


@router.get("/{campaign_id}/tasks", response_model=list[CampaignTaskResponse])
def get_tasks(campaign_id: int, db: Session = Depends(get_db)):
    _campaign_or_404(db, campaign_id)
    return list_campaign_tasks(db, campaign_id)


@router.get("/{campaign_id}/tasks/{task_id}", response_model=CampaignTaskDetailResponse)
def get_task(campaign_id: int, task_id: int, db: Session = Depends(get_db)):
    _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    return task


@router.patch("/{campaign_id}/tasks/{task_id}", response_model=CampaignTaskDetailResponse)
def patch_task(campaign_id: int, task_id: int, payload: CampaignTaskUpdate, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    try:
        return CampaignTaskService().update_task(db, campaign, task, payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid task update") from exc


@router.post("/{campaign_id}/tasks/{task_id}/start", response_model=CampaignTaskDetailResponse)
def start_task(campaign_id: int, task_id: int, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    try:
        return CampaignTaskService().start(db, campaign, task)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{campaign_id}/tasks/{task_id}/block", response_model=CampaignTaskDetailResponse)
def block_task(campaign_id: int, task_id: int, payload: CampaignTaskBlockRequest, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    try:
        return CampaignTaskService().block(db, campaign, task, payload.blocked_reason)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{campaign_id}/tasks/{task_id}/unblock", response_model=CampaignTaskDetailResponse)
def unblock_task(campaign_id: int, task_id: int, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    try:
        return CampaignTaskService().unblock(db, campaign, task)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{campaign_id}/tasks/{task_id}/review", response_model=CampaignTaskDetailResponse)
def review_task(campaign_id: int, task_id: int, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    try:
        return CampaignTaskService().review(db, campaign, task)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{campaign_id}/tasks/{task_id}/complete", response_model=CampaignTaskDetailResponse)
def complete_task(
    campaign_id: int,
    task_id: int,
    payload: CampaignTaskCompleteRequest,
    db: Session = Depends(get_db),
):
    campaign = _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    try:
        return CampaignTaskService().complete(
            db,
            campaign,
            task,
            completion_notes=payload.completion_notes,
            actual_hours=payload.actual_hours,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{campaign_id}/tasks/{task_id}/cancel", response_model=CampaignTaskDetailResponse)
def cancel_task(campaign_id: int, task_id: int, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    try:
        return CampaignTaskService().cancel(db, campaign, task)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{campaign_id}/tasks/{task_id}/reopen", response_model=CampaignTaskDetailResponse)
def reopen_task(
    campaign_id: int,
    task_id: int,
    payload: CampaignTaskReopenRequest,
    db: Session = Depends(get_db),
):
    campaign = _campaign_or_404(db, campaign_id)
    task = _task_or_404(db, campaign_id, task_id)
    try:
        return CampaignTaskService().reopen(db, campaign, task, payload.reason)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{campaign_id}/assets", response_model=list[CampaignAssetResponse])
def get_assets(campaign_id: int, db: Session = Depends(get_db)):
    _campaign_or_404(db, campaign_id)
    return list_campaign_assets(db, campaign_id)


@router.post("/{campaign_id}/approve", response_model=CampaignResponse)
def approve(campaign_id: int, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    try:
        CampaignStatusService().transition(campaign, "approved")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid campaign status transition") from exc
    CampaignService().repair_task_readiness(db, campaign)
    campaign.progress = CampaignProgressService().build_progress(db, campaign)
    return update_campaign(db, campaign)


@router.post("/{campaign_id}/repair-readiness", response_model=CampaignResponse)
def repair_readiness(campaign_id: int, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    CampaignService().repair_task_readiness(db, campaign)
    campaign.progress = CampaignProgressService().build_progress(db, campaign)
    return update_campaign(db, campaign)


@router.post("/{campaign_id}/status", response_model=CampaignResponse)
def change_status(campaign_id: int, status: str = Query(...), db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    try:
        CampaignStatusService().transition(campaign, status)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid campaign status transition") from exc
    if status in {"approved", "building"}:
        CampaignService().repair_task_readiness(db, campaign)
    campaign.progress = CampaignProgressService().build_progress(db, campaign)
    return update_campaign(db, campaign)


@router.get("/{campaign_id}/progress")
def progress(campaign_id: int, db: Session = Depends(get_db)):
    campaign = _campaign_or_404(db, campaign_id)
    return CampaignProgressService().build_progress(db, campaign)
