from collections.abc import Sequence

from app.services.opportunities.evidence_scoring import calculate_scores_from_evidence
from app.services.research.signals import ResearchEvidenceItem, ResearchSignals


def score_evidence_items(
    evidence_items: Sequence[ResearchEvidenceItem],
) -> ResearchSignals:
    scores = calculate_scores_from_evidence(evidence_items)
    return ResearchSignals(
        demand=scores.demand_score,
        competition=scores.competition_score,
        buyer_intent=scores.buyer_intent_score,
        affiliate_potential=scores.affiliate_score,
        pinterest_potential=scores.pinterest_score,
        seo_potential=scores.seo_score,
    )
