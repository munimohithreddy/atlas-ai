from typing import Literal
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
    campaign_task_id: int | None = None
    asset_type: str
    title: str
    description: str | None = None
    channel: str
    status: str
    priority: str
    content_brief: str | None = None
    target_audience: str | None = None
    primary_keyword: str | None = None
    secondary_keywords: str | None = None
    call_to_action: str | None = None
    assigned_to: str | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None
    due_date: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    blocked_reason: str | None = None
    review_notes: str | None = None
    rejection_reason: str | None = None
    approved_at: datetime | None = None
    order_index: int
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
    total_assets: int | None = None
    planned_assets: int | None = None
    queued_assets: int | None = None
    in_production_assets: int | None = None
    review_assets: int | None = None
    approved_assets: int | None = None
    ready_to_publish_assets: int | None = None
    blocked_assets: int | None = None
    rejected_assets: int | None = None
    asset_completion_percentage: int | None = None

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


AssetStatus = Literal[
    "planned",
    "queued",
    "in_production",
    "review",
    "approved",
    "ready_to_publish",
    "blocked",
    "rejected",
    "cancelled",
]

AssetType = Literal[
    "homepage",
    "buying_guide",
    "comparison_page",
    "product_review",
    "blog_post",
    "pinterest_pin",
    "youtube_short",
    "email",
    "landing_page",
    "social_post",
]

AssetChannel = Literal["website", "pinterest", "youtube", "email", "social"]

AssetPriority = Literal["low", "medium", "high", "critical"]


class CampaignAssetCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None
    asset_type: AssetType
    channel: AssetChannel
    priority: AssetPriority = "medium"
    content_brief: str | None = None
    target_audience: str | None = None
    primary_keyword: str | None = None
    secondary_keywords: list[str] | None = None
    call_to_action: str | None = None
    assigned_to: str | None = None
    estimated_hours: float | None = Field(default=None, ge=0)
    actual_hours: float | None = Field(default=None, ge=0)
    due_date: datetime | None = None
    campaign_task_id: int | None = None
    order_index: int | None = None


class CampaignAssetUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    asset_type: AssetType | None = None
    channel: AssetChannel | None = None
    status: AssetStatus | None = None
    priority: AssetPriority | None = None
    content_brief: str | None = None
    target_audience: str | None = None
    primary_keyword: str | None = None
    secondary_keywords: list[str] | None = None
    call_to_action: str | None = None
    assigned_to: str | None = None
    estimated_hours: float | None = Field(default=None, ge=0)
    actual_hours: float | None = Field(default=None, ge=0)
    due_date: datetime | None = None
    campaign_task_id: int | None = None
    order_index: int | None = None


class CampaignAssetBlockRequest(BaseModel):
    blocked_reason: str = Field(..., min_length=2)


class CampaignAssetReviewRequest(BaseModel):
    review_notes: str | None = None


class CampaignAssetRejectRequest(BaseModel):
    rejection_reason: str | None = None
    review_notes: str | None = None

