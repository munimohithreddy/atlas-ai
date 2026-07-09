from collections.abc import Sequence

from sqlalchemy.orm import Session, selectinload

from app.models.opportunity import Opportunity
from app.models.opportunity_evidence import OpportunityEvidence
from app.schemas.opportunity import OpportunityCreate, OpportunityEvidenceCreate
from app.services.research.analysis import OpportunityAIAnalysis
from app.services.opportunities.scoring import (
    build_reasoning,
    calculate_opportunity_score,
    make_recommendation,
)


def create_opportunity(
    db: Session,
    payload: OpportunityCreate,
    evidence_items: Sequence[OpportunityEvidenceCreate] | None = None,
) -> Opportunity:
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

    if evidence_items:
        evidence_rows = [
            OpportunityEvidence(
                opportunity_id=opportunity.id,
                source=item.source,
                signal_type=item.signal_type,
                value=item.value,
                summary=item.summary,
                confidence_score=item.confidence_score,
            )
            for item in evidence_items
        ]
        for evidence in evidence_rows:
            db.add(evidence)
        db.commit()
        for evidence in evidence_rows:
            db.refresh(evidence)
        opportunity.evidence = evidence_rows

    return opportunity


def get_opportunity(db: Session, opportunity_id: int) -> Opportunity | None:
    return (
        db.query(Opportunity)
        .options(selectinload(Opportunity.evidence))
        .filter(Opportunity.id == opportunity_id)
        .first()
    )


def update_opportunity_analysis(
    db: Session,
    opportunity: Opportunity,
    analysis: OpportunityAIAnalysis,
) -> Opportunity:
    opportunity.ai_executive_summary = analysis.executive_summary
    opportunity.ai_key_strengths = analysis.key_strengths
    opportunity.ai_key_risks = analysis.key_risks
    opportunity.ai_recommendation_reason = analysis.recommendation_reason
    opportunity.ai_suggested_next_actions = analysis.suggested_next_actions

    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity


def list_opportunities(db: Session) -> list[Opportunity]:
    return db.query(Opportunity).order_by(Opportunity.created_at.desc()).all()
