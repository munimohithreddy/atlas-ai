from dataclasses import dataclass

from app.schemas.opportunity import OpportunityCreate, OpportunityEvidenceCreate
from app.services.research.mock_provider import MockResearchProvider


@dataclass(frozen=True)
class ResearchOpportunityEvaluation:
    opportunity: OpportunityCreate
    evidence: tuple[OpportunityEvidenceCreate, ...]


def build_opportunity_from_research(
    topic: str,
    niche: str | None = None,
    provider: MockResearchProvider | None = None,
) -> ResearchOpportunityEvaluation:
    research_provider = provider or MockResearchProvider()
    result = research_provider.research(topic=topic, niche=niche)
    signals = result.signals

    opportunity = OpportunityCreate(
        topic=topic,
        niche=niche,
        demand_score=signals.demand,
        competition_score=signals.competition,
        buyer_intent_score=signals.buyer_intent,
        affiliate_score=signals.affiliate_potential,
        pinterest_score=signals.pinterest_potential,
        seo_score=signals.seo_potential,
    )
    evidence = tuple(
        OpportunityEvidenceCreate(
            source=item.source,
            signal_type=item.signal_type,
            value=item.value,
            summary=item.summary,
            confidence_score=item.confidence_score,
        )
        for item in result.evidence
    )

    return ResearchOpportunityEvaluation(opportunity=opportunity, evidence=evidence)
