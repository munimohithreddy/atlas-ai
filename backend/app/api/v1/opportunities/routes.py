from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.repositories.opportunity_repository import (
    create_opportunity,
    list_opportunities,
)
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityEvaluateRequest,
    OpportunityResponse,
)
from app.services.research import build_opportunity_from_research

router = APIRouter(prefix='/opportunities', tags=['opportunities'])


@router.post('', response_model=OpportunityResponse)
def create(payload: OpportunityCreate, db: Session = Depends(get_db)):
    return create_opportunity(db, payload)


@router.post('/evaluate', response_model=OpportunityResponse)
def evaluate(payload: OpportunityEvaluateRequest, db: Session = Depends(get_db)):
    researched_payload = build_opportunity_from_research(
        topic=payload.topic,
        niche=payload.niche,
    )
    return create_opportunity(db, researched_payload)


@router.get('', response_model=list[OpportunityResponse])
def list_all(db: Session = Depends(get_db)):
    return list_opportunities(db)
