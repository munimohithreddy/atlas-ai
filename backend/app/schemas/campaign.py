from datetime import datetime

from pydantic import BaseModel, Field


class CampaignCreate(BaseModel):
    business_plan_id: int
    goal: str | None = None
    priority: str | None = Field(default="medium")
    launch_target_date: datetime | None = None


class CampaignUpdate(BaseModel):
    name: str | None = None
    goal: str | None = None
    status: str | None = None
    priority: str | None = None
    expected_monthly_revenue: int | None = None
    estimated_build_hours: int | None = None
    launch_target_date: datetime | None = None


class CampaignTaskResponse(BaseModel):
    id: int
    campaign_id: int
    title: str
    description: str | None
    category: str
    status: str
    priority: str
    estimated_hours: int
    started_at: datetime | None = None
    completed_at: datetime | None = None
    blocked_reason: str | None = None
    completion_notes: str | None = None
    actual_hours: float | None = None
    assigned_to: str | None = None
    due_date: datetime | None = None
    depends_on_task_id: int | None
    order_index: int

    class Config:
        from_attributes = True


class CampaignTaskDetailResponse(CampaignTaskResponse):
    pass


class CampaignAssetResponse(BaseModel):
    id: int
    campaign_id: int
    asset_type: str
    title: str
    channel: str
    status: str
    planned_quantity: int
    generated_quantity: int
    published_quantity: int

    class Config:
        from_attributes = True


class CampaignResponse(BaseModel):
    id: int
    business_plan_id: int
    brand_id: int | None
    opportunity_id: int
    name: str
    slug: str
    goal: str
    status: str
    priority: str
    expected_monthly_revenue: int
    estimated_build_hours: int
    launch_target_date: datetime | None
    approved_at: datetime | None
    progress: dict[str, object] | None = None

    class Config:
        from_attributes = True


class CampaignDetailResponse(CampaignResponse):
    tasks: list[CampaignTaskResponse]
    assets: list[CampaignAssetResponse]


class CampaignTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    estimated_hours: int | None = None
    actual_hours: float | None = Field(default=None, ge=0)
    assigned_to: str | None = None
    due_date: datetime | None = None
    order_index: int | None = None


class CampaignTaskStatusRequest(BaseModel):
    status: str


class CampaignTaskBlockRequest(BaseModel):
    blocked_reason: str = Field(..., min_length=2)


class CampaignTaskCompleteRequest(BaseModel):
    completion_notes: str | None = None
    actual_hours: float | None = Field(default=None, ge=0)


class CampaignTaskReopenRequest(BaseModel):
    reason: str = Field(..., min_length=2)

