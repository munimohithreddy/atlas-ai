from app.schemas.opportunity import OpportunityCreate
from app.services.research.mock_provider import MockResearchProvider


def build_opportunity_from_research(
    topic: str,
    niche: str | None = None,
    provider: MockResearchProvider | None = None,
) -> OpportunityCreate:
    research_provider = provider or MockResearchProvider()
    signals = research_provider.research(topic=topic, niche=niche)

    return OpportunityCreate(
        topic=topic,
        niche=niche,
        demand_score=signals.demand,
        competition_score=signals.competition,
        buyer_intent_score=signals.buyer_intent,
        affiliate_score=signals.affiliate_potential,
        pinterest_score=signals.pinterest_potential,
        seo_score=signals.seo_potential,
    )
