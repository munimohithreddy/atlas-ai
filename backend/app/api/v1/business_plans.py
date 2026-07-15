from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.repositories.business_plan_repository import get_business_plan, list_business_plans
from app.repositories.opportunity_repository import get_opportunity
from app.schemas.business_plan import BusinessPlanCreateRequest, BusinessPlanResponse
from app.services.business_planning.business_plan import BusinessPlanService

router = APIRouter(prefix="/business-plans", tags=["business-plans"])


@router.post("/opportunities/{opportunity_id}", response_model=BusinessPlanResponse)
def create_for_opportunity(
    opportunity_id: int,
    payload: BusinessPlanCreateRequest,
    db: Session = Depends(get_db),
):
    opportunity = get_opportunity(db, opportunity_id)
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    service = BusinessPlanService()
    return service.create_plan(
        db=db,
        opportunity=opportunity,
        brand_id=payload.brand_id,
        brand_name=payload.brand_name,
        constraints=payload.user_constraints,
    )


@router.get("", response_model=list[BusinessPlanResponse])
def list_all(offset: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return list_business_plans(db, offset=offset, limit=limit)


@router.get("/{business_plan_id}", response_model=BusinessPlanResponse)
def get_by_id(business_plan_id: int, db: Session = Depends(get_db)):
    business_plan = get_business_plan(db, business_plan_id)
    if business_plan is None:
        raise HTTPException(status_code=404, detail="Business plan not found")
    return business_plan
