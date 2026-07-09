from pydantic import BaseModel, Field


class ResearchPreviewRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=255)
    niche: str | None = None


class ResearchEvidencePreviewResponse(BaseModel):
    source: str
    signal_type: str
    value: int
    summary: str
    confidence_score: int


class ResearchPreviewResponse(BaseModel):
    topic: str
    niche: str | None
    evidence: list[ResearchEvidencePreviewResponse]
