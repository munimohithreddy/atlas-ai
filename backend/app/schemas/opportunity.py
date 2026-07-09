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
    confidence_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Integer confidence score from 0 to 100.",
    )


class OpportunityEvaluateWithEvidenceRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=255)
    niche: str | None = None
    evidence_items: list[OpportunityEvidenceCreate] = Field(..., min_length=1)


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
    ai_executive_summary: str | None = None
    ai_key_strengths: list[str] | None = None
    ai_key_risks: list[str] | None = None
    ai_recommendation_reason: str | None = None
    ai_suggested_next_actions: list[str] | None = None
    evidence: list[OpportunityEvidenceResponse]
