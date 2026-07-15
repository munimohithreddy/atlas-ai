from pydantic import BaseModel, Field


class BusinessPlanConstraints(BaseModel):
    monthly_budget: int | None = Field(default=None, ge=0)
    hours_per_week: int | None = Field(default=None, ge=0)
    target_monthly_revenue: int | None = Field(default=None, ge=0)


class BusinessPlanCreateRequest(BaseModel):
    brand_id: int | None = None
    brand_name: str | None = Field(default=None, min_length=2, max_length=255)
    user_constraints: BusinessPlanConstraints | None = None


class BusinessPlanResponse(BaseModel):
    id: int
    opportunity_id: int
    brand_id: int | None
    primary_monetization: str
    secondary_monetization: str | None
    primary_acquisition_channel: str
    secondary_acquisition_channels: list[str]
    recommended_assets: list[str]
    target_audience: str
    value_proposition: str
    revenue_low_monthly: int
    revenue_high_monthly: int
    revenue_confidence_score: int
    effort_level: str
    estimated_launch_days: int
    recommendation_summary: str
    next_action: str
    status: str

    class Config:
        from_attributes = True

