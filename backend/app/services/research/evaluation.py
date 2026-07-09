from dataclasses import dataclass
from collections.abc import Sequence

from app.integrations.search import ManualEvidenceSearchProvider, SearchResearchProvider
from app.schemas.opportunity import OpportunityCreate, OpportunityEvidenceCreate
from app.services.opportunities.evidence_scoring import calculate_scores_from_evidence
from app.services.research.mock_provider import MockResearchProvider
from app.services.research.signals import ResearchEvidenceItem


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
    opportunity = _build_opportunity_from_evidence(
        topic=topic,
        niche=niche,
        evidence=evidence,
    )

    return ResearchOpportunityEvaluation(opportunity=opportunity, evidence=evidence)


def build_opportunity_from_manual_evidence(
    topic: str,
    niche: str | None,
    evidence_items: Sequence[OpportunityEvidenceCreate],
    provider: SearchResearchProvider | None = None,
) -> ResearchOpportunityEvaluation:
    research_provider = provider or ManualEvidenceSearchProvider()
    submitted_evidence = tuple(
        ResearchEvidenceItem(
            source=item.source,
            signal_type=item.signal_type,
            value=item.value,
            summary=item.summary,
            confidence_score=item.confidence_score,
        )
        for item in evidence_items
    )
    result = research_provider.research(
        topic=topic,
        niche=niche,
        evidence_items=submitted_evidence,
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
    opportunity = _build_opportunity_from_evidence(
        topic=topic,
        niche=niche,
        evidence=evidence,
    )

    return ResearchOpportunityEvaluation(opportunity=opportunity, evidence=evidence)


def _build_opportunity_from_evidence(
    topic: str,
    niche: str | None,
    evidence: Sequence[OpportunityEvidenceCreate],
) -> OpportunityCreate:
    scores = calculate_scores_from_evidence(evidence)
    return OpportunityCreate(
        topic=topic,
        niche=niche,
        demand_score=scores.demand_score,
        competition_score=scores.competition_score,
        buyer_intent_score=scores.buyer_intent_score,
        affiliate_score=scores.affiliate_score,
        pinterest_score=scores.pinterest_score,
        seo_score=scores.seo_score,
    )
