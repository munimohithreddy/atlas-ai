from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.repositories.opportunity_repository import (
    create_opportunity,
    get_opportunity,
    list_opportunities,
    update_opportunity_analysis,
)
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityEvaluateRequest,
    OpportunityEvaluateWithEvidenceRequest,
    OpportunityPortfolioRequest,
    OpportunityPortfolioResponse,
    OpportunityResponse,
    OpportunityWithEvidenceResponse,
)
from app.services.opportunities.portfolio import evaluate_opportunity_portfolio
from app.services.research import (
    build_opportunity_from_manual_evidence,
    build_opportunity_from_research,
)
from app.services.research.analysis import (
    build_score_snapshot,
    synthesize_opportunity_analysis,
)
from app.schemas.business_plan import BusinessPlanCreateRequest, BusinessPlanResponse
from app.services.business_planning.business_plan import BusinessPlanService

router = APIRouter(prefix='/opportunities', tags=['opportunities'])


@router.post('', response_model=OpportunityResponse)
def create(payload: OpportunityCreate, db: Session = Depends(get_db)):
    return create_opportunity(db, payload)


@router.post('/evaluate', response_model=OpportunityResponse)
def evaluate(payload: OpportunityEvaluateRequest, db: Session = Depends(get_db)):
    evaluation = build_opportunity_from_research(
        topic=payload.topic,
        niche=payload.niche,
    )
    return create_opportunity(
        db,
        evaluation.opportunity,
        evidence_items=evaluation.evidence,
    )


@router.post('/evaluate-with-evidence', response_model=OpportunityResponse)
def evaluate_with_evidence(
    payload: OpportunityEvaluateWithEvidenceRequest,
    db: Session = Depends(get_db),
):
    evaluation = build_opportunity_from_manual_evidence(
        topic=payload.topic,
        niche=payload.niche,
        evidence_items=payload.evidence_items,
    )
    opportunity = create_opportunity(
        db,
        evaluation.opportunity,
        evidence_items=evaluation.evidence,
    )
    analysis = synthesize_opportunity_analysis(
        topic=payload.topic,
        niche=payload.niche,
        evidence_items=evaluation.evidence,
        scores=build_score_snapshot(opportunity),
    )
    return update_opportunity_analysis(db, opportunity, analysis)


@router.post('/portfolio', response_model=OpportunityPortfolioResponse)
def portfolio(payload: OpportunityPortfolioRequest):
    return {
        "results": evaluate_opportunity_portfolio(
            topics=payload.topics,
            niche=payload.niche,
        )
    }


@router.get('/{opportunity_id}', response_model=OpportunityWithEvidenceResponse)
def get_by_id(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = get_opportunity(db, opportunity_id)
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity


@router.get('', response_model=list[OpportunityResponse])
def list_all(db: Session = Depends(get_db)):
    return list_opportunities(db)


@router.post('/{opportunity_id}/business-plan', response_model=BusinessPlanResponse)
def create_business_plan(
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
