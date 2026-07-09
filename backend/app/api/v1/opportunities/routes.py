from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.repositories.opportunity_repository import (
    create_opportunity,
    list_opportunities,
)
from app.schemas.opportunity import OpportunityCreate, OpportunityResponse

router = APIRouter(prefix='/opportunities', tags=['opportunities'])


@router.post('', response_model=OpportunityResponse)
def create(payload: OpportunityCreate, db: Session = Depends(get_db)):
    return create_opportunity(db, payload)


@router.get('', response_model=list[OpportunityResponse])
def list_all(db: Session = Depends(get_db)):
    return list_opportunities(db)
