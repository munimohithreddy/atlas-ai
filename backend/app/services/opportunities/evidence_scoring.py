from collections.abc import Sequence
from dataclasses import dataclass


SIGNAL_TO_SCORE_FIELD = {
    "demand": "demand_score",
    "competition": "competition_score",
    "buyer_intent": "buyer_intent_score",
    "affiliate": "affiliate_score",
    "affiliate_potential": "affiliate_score",
    "pinterest": "pinterest_score",
    "pinterest_potential": "pinterest_score",
    "seo": "seo_score",
    "seo_potential": "seo_score",
}

NEUTRAL_DEFAULT_SCORE = 50


@dataclass(frozen=True)
class EvidenceBasedOpportunityScores:
    demand_score: int
    competition_score: int
    buyer_intent_score: int
    affiliate_score: int
    pinterest_score: int
    seo_score: int


def calculate_scores_from_evidence(
    evidence_items: Sequence[object],
) -> EvidenceBasedOpportunityScores:
    grouped: dict[str, list[object]] = {
        "demand_score": [],
        "competition_score": [],
        "buyer_intent_score": [],
        "affiliate_score": [],
        "pinterest_score": [],
        "seo_score": [],
    }

    for item in evidence_items:
        score_field = SIGNAL_TO_SCORE_FIELD.get(getattr(item, "signal_type"))
        if score_field is not None:
            grouped[score_field].append(item)

    scores = {
        score_field: (
            _confidence_weighted_average(items)
            if items
            else NEUTRAL_DEFAULT_SCORE
        )
        for score_field, items in grouped.items()
    }

    return EvidenceBasedOpportunityScores(
        demand_score=scores["demand_score"],
        competition_score=scores["competition_score"],
        buyer_intent_score=scores["buyer_intent_score"],
        affiliate_score=scores["affiliate_score"],
        pinterest_score=scores["pinterest_score"],
        seo_score=scores["seo_score"],
    )


def _confidence_weighted_average(items: Sequence[object]) -> int:
    total_confidence = sum(getattr(item, "confidence_score") for item in items)
    if total_confidence <= 0:
        return round(sum(getattr(item, "value") for item in items) / len(items))

    weighted_total = sum(
        getattr(item, "value") * getattr(item, "confidence_score")
        for item in items
    )
    return round(weighted_total / total_confidence)
