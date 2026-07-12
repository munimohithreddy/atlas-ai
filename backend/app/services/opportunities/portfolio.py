from dataclasses import dataclass

from app.services.opportunities.evidence_scoring import calculate_scores_from_evidence
from app.services.opportunities.scoring import (
    calculate_opportunity_score,
    make_recommendation,
)
from app.services.research import ResearchOrchestrator


@dataclass(frozen=True)
class PortfolioOpportunity:
    rank: int
    topic: str
    business_score: float
    recommendation: str
    confidence: int
    demand_score: int
    competition_score: int
    buyer_intent_score: int
    affiliate_score: int
    pinterest_score: int
    seo_score: int


def evaluate_opportunity_portfolio(
    topics: list[str],
    niche: str | None = None,
    orchestrator: ResearchOrchestrator | None = None,
) -> tuple[PortfolioOpportunity, ...]:
    research_orchestrator = orchestrator or ResearchOrchestrator()
    evaluated = [
        _evaluate_topic(
            topic=topic,
            niche=niche,
            orchestrator=research_orchestrator,
        )
        for topic in topics
    ]
    ranked = sorted(evaluated, key=lambda item: item.business_score, reverse=True)

    return tuple(
        PortfolioOpportunity(
            rank=index,
            topic=item.topic,
            business_score=item.business_score,
            recommendation=item.recommendation,
            confidence=item.confidence,
            demand_score=item.demand_score,
            competition_score=item.competition_score,
            buyer_intent_score=item.buyer_intent_score,
            affiliate_score=item.affiliate_score,
            pinterest_score=item.pinterest_score,
            seo_score=item.seo_score,
        )
        for index, item in enumerate(ranked, start=1)
    )


def _evaluate_topic(
    topic: str,
    niche: str | None,
    orchestrator: ResearchOrchestrator,
) -> PortfolioOpportunity:
    evidence = orchestrator.collect_evidence(topic=topic, niche=niche)
    scores = calculate_scores_from_evidence(evidence)
    business_score = calculate_opportunity_score(
        demand_score=scores.demand_score,
        competition_score=scores.competition_score,
        buyer_intent_score=scores.buyer_intent_score,
        affiliate_score=scores.affiliate_score,
        pinterest_score=scores.pinterest_score,
        seo_score=scores.seo_score,
    )

    return PortfolioOpportunity(
        rank=0,
        topic=topic,
        business_score=business_score,
        recommendation=make_recommendation(business_score),
        confidence=_calculate_confidence(evidence),
        demand_score=scores.demand_score,
        competition_score=scores.competition_score,
        buyer_intent_score=scores.buyer_intent_score,
        affiliate_score=scores.affiliate_score,
        pinterest_score=scores.pinterest_score,
        seo_score=scores.seo_score,
    )


def _calculate_confidence(evidence: tuple[object, ...]) -> int:
    if not evidence:
        return 0
    return round(
        sum(item.confidence_score for item in evidence) / len(evidence)
    )
