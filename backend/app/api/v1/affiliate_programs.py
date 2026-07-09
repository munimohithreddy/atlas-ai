from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.repositories.affiliate_program_repository import (
    create_affiliate_program,
    get_affiliate_program,
    list_affiliate_programs,
)
from app.schemas.affiliate_program import (
    AffiliateProgramCreate,
    AffiliateProgramResponse,
)

router = APIRouter(prefix="/affiliate-programs", tags=["affiliate-programs"])


@router.post("", response_model=AffiliateProgramResponse)
def create(payload: AffiliateProgramCreate, db: Session = Depends(get_db)):
    return create_affiliate_program(db, payload)


@router.get("", response_model=list[AffiliateProgramResponse])
def list_all(db: Session = Depends(get_db)):
    return list_affiliate_programs(db)


@router.get("/{program_id}", response_model=AffiliateProgramResponse)
def get_by_id(program_id: int, db: Session = Depends(get_db)):
    program = get_affiliate_program(db, program_id)
    if program is None:
        raise HTTPException(status_code=404, detail="Affiliate program not found")
    return program
