from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.repositories.brand_repository import create_brand, get_brand, list_brands
from app.schemas.brand import BrandCreate, BrandResponse

router = APIRouter(prefix="/brands", tags=["brands"])


@router.post("", response_model=BrandResponse)
def create(payload: BrandCreate, db: Session = Depends(get_db)):
    try:
        return create_brand(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Brand slug already exists") from exc


@router.get("", response_model=list[BrandResponse])
def list_all(db: Session = Depends(get_db)):
    return list_brands(db)


@router.get("/{brand_id}", response_model=BrandResponse)
def get_by_id(brand_id: int, db: Session = Depends(get_db)):
    brand = get_brand(db, brand_id)
    if brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand
