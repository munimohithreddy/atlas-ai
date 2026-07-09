from sqlalchemy.orm import Session

from app.models.affiliate_program import AffiliateProgram
from app.schemas.affiliate_program import AffiliateProgramCreate


def create_affiliate_program(
    db: Session,
    payload: AffiliateProgramCreate,
) -> AffiliateProgram:
    program = AffiliateProgram(
        name=payload.name,
        network=payload.network,
        category=payload.category,
        website_url=payload.website_url,
        commission_type=payload.commission_type,
        commission_rate=payload.commission_rate,
        cookie_duration_days=payload.cookie_duration_days,
        approval_required=payload.approval_required,
        notes=payload.notes,
    )

    db.add(program)
    db.commit()
    db.refresh(program)
    return program


def get_affiliate_program(db: Session, program_id: int) -> AffiliateProgram | None:
    return (
        db.query(AffiliateProgram)
        .filter(AffiliateProgram.id == program_id)
        .first()
    )


def list_affiliate_programs(db: Session) -> list[AffiliateProgram]:
    return db.query(AffiliateProgram).order_by(AffiliateProgram.created_at.desc()).all()
