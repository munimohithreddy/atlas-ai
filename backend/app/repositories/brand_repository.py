from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.schemas.brand import BrandCreate


def create_brand(db: Session, payload: BrandCreate) -> Brand:
    existing = db.query(Brand).filter(Brand.slug == payload.slug).first()
    if existing is not None:
        raise ValueError("Brand slug already exists")

    brand = Brand(
        name=payload.name,
        slug=payload.slug,
        market=payload.market,
        description=payload.description,
        status=payload.status,
    )
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


def get_brand(db: Session, brand_id: int) -> Brand | None:
    return db.query(Brand).filter(Brand.id == brand_id).first()


def get_brand_by_slug(db: Session, slug: str) -> Brand | None:
    return db.query(Brand).filter(Brand.slug == slug).first()


def list_brands(db: Session) -> list[Brand]:
    return db.query(Brand).order_by(Brand.created_at.desc()).all()
