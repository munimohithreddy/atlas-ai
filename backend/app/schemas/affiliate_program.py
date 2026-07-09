from pydantic import BaseModel, Field


class AffiliateProgramCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    network: str = Field(..., min_length=2, max_length=255)
    category: str = Field(..., min_length=2, max_length=255)
    website_url: str = Field(..., min_length=5, max_length=500)
    commission_type: str = Field(..., min_length=2, max_length=100)
    commission_rate: float = Field(..., ge=0)
    cookie_duration_days: int = Field(..., ge=0)
    approval_required: bool = True
    notes: str | None = None


class AffiliateProgramResponse(BaseModel):
    id: int
    name: str
    network: str
    category: str
    website_url: str
    commission_type: str
    commission_rate: float
    cookie_duration_days: int
    approval_required: bool
    notes: str | None

    class Config:
        from_attributes = True
