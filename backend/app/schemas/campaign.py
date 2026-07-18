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
    depends_on_task_id: int | None
    order_index: int

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


class CampaignDetailResponse(CampaignResponse):
    tasks: list[CampaignTaskResponse]
    assets: list[CampaignAssetResponse]

