from pydantic import BaseModel, Field


class OpportunityCreate(BaseModel):
    topic: str = Field(..., min_length=2, max_length=255)
    niche: str | None = None

    demand_score: int = Field(..., ge=0, le=100)
    competition_score: int = Field(..., ge=0, le=100)
    buyer_intent_score: int = Field(..., ge=0, le=100)
    affiliate_score: int = Field(..., ge=0, le=100)
    pinterest_score: int = Field(..., ge=0, le=100)
    seo_score: int = Field(..., ge=0, le=100)


class OpportunityEvaluateRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=255)
    niche: str | None = None


class OpportunityEvidenceCreate(BaseModel):
    source: str = Field(..., min_length=2, max_length=100)
    signal_type: str = Field(..., min_length=2, max_length=100)
    value: int = Field(..., ge=0, le=100)
    summary: str = Field(..., min_length=2)
    confidence_score: int = Field(..., ge=0, le=100)


class OpportunityEvidenceResponse(BaseModel):
    id: int
    opportunity_id: int
    source: str
    signal_type: str
    value: int
    summary: str
    confidence_score: int

    class Config:
        from_attributes = True


class OpportunityResponse(BaseModel):
    id: int
    topic: str
    niche: str | None

    demand_score: int
    competition_score: int
    buyer_intent_score: int
    affiliate_score: int
    pinterest_score: int
    seo_score: int

    opportunity_score: float
    recommendation: str
    reasoning: str

    class Config:
        from_attributes = True


class OpportunityWithEvidenceResponse(OpportunityResponse):
    evidence: list[OpportunityEvidenceResponse]
