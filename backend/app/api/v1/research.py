from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.repositories.affiliate_program_repository import list_affiliate_programs
from app.schemas.research import ResearchPreviewRequest, ResearchPreviewResponse
from app.services.research import (
    AffiliateProgramResearchProvider,
    MockResearchProvider,
    ResearchOrchestrator,
)

router = APIRouter(prefix="/research", tags=["research"])


@router.post("/preview", response_model=ResearchPreviewResponse)
def preview(payload: ResearchPreviewRequest, db: Session = Depends(get_db)):
    programs = list_affiliate_programs(db)
    evidence = ResearchOrchestrator(
        providers=(
            MockResearchProvider(),
            AffiliateProgramResearchProvider(programs),
        )
    ).collect_evidence(
        topic=payload.topic,
        niche=payload.niche,
    )
    return {
        "topic": payload.topic,
        "niche": payload.niche,
        "evidence": evidence,
    }
