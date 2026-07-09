from sqlalchemy.orm import Session

from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate
from app.services.opportunities.scoring import (
    build_reasoning,
    calculate_opportunity_score,
    make_recommendation,
)


def create_opportunity(db: Session, payload: OpportunityCreate) -> Opportunity:
    score = calculate_opportunity_score(
        demand_score=payload.demand_score,
        competition_score=payload.competition_score,
        buyer_intent_score=payload.buyer_intent_score,
        affiliate_score=payload.affiliate_score,
        pinterest_score=payload.pinterest_score,
        seo_score=payload.seo_score,
    )

    recommendation = make_recommendation(score)

    opportunity = Opportunity(
        topic=payload.topic,
        niche=payload.niche,
        demand_score=payload.demand_score,
        competition_score=payload.competition_score,
        buyer_intent_score=payload.buyer_intent_score,
        affiliate_score=payload.affiliate_score,
        pinterest_score=payload.pinterest_score,
        seo_score=payload.seo_score,
        opportunity_score=score,
        recommendation=recommendation,
        reasoning=build_reasoning(
            topic=payload.topic,
            score=score,
            recommendation=recommendation,
            demand_score=payload.demand_score,
            competition_score=payload.competition_score,
            buyer_intent_score=payload.buyer_intent_score,
            affiliate_score=payload.affiliate_score,
            pinterest_score=payload.pinterest_score,
            seo_score=payload.seo_score,
        ),
    )

    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity


def list_opportunities(db: Session) -> list[Opportunity]:
    return db.query(Opportunity).order_by(Opportunity.created_at.desc()).all()
