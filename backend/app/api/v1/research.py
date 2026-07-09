from fastapi import APIRouter

from app.schemas.research import ResearchPreviewRequest, ResearchPreviewResponse
from app.services.research import ResearchOrchestrator

router = APIRouter(prefix="/research", tags=["research"])


@router.post("/preview", response_model=ResearchPreviewResponse)
def preview(payload: ResearchPreviewRequest):
    evidence = ResearchOrchestrator().collect_evidence(
        topic=payload.topic,
        niche=payload.niche,
    )
    return {
        "topic": payload.topic,
        "niche": payload.niche,
        "evidence": evidence,
    }
