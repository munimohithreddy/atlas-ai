from sqlalchemy.orm import Session, selectinload

from app.models.business_plan import BusinessPlan
from app.schemas.business_plan import BusinessPlanResponse


def create_business_plan(db: Session, business_plan: BusinessPlan) -> BusinessPlan:
    db.add(business_plan)
    db.commit()
    db.refresh(business_plan)
    return business_plan


def get_business_plan(db: Session, business_plan_id: int) -> BusinessPlan | None:
    return (
        db.query(BusinessPlan)
        .options(selectinload(BusinessPlan.brand), selectinload(BusinessPlan.opportunity))
        .filter(BusinessPlan.id == business_plan_id)
        .first()
    )


def list_business_plans(db: Session, offset: int = 0, limit: int = 20) -> list[BusinessPlan]:
    return (
        db.query(BusinessPlan)
        .options(selectinload(BusinessPlan.brand), selectinload(BusinessPlan.opportunity))
        .order_by(BusinessPlan.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
