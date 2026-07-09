from collections.abc import Sequence

from app.services.research.signals import ResearchEvidenceItem, ResearchSignals


SIGNAL_ALIASES = {
    "demand": "demand",
    "competition": "competition",
    "buyer_intent": "buyer_intent",
    "affiliate": "affiliate_potential",
    "affiliate_potential": "affiliate_potential",
    "pinterest": "pinterest_potential",
    "pinterest_potential": "pinterest_potential",
    "seo": "seo_potential",
    "seo_potential": "seo_potential",
}

DEFAULT_SIGNAL_SCORES = {
    "demand": 50,
    "competition": 50,
    "buyer_intent": 50,
    "affiliate_potential": 50,
    "pinterest_potential": 50,
    "seo_potential": 50,
}


def _weighted_average(items: Sequence[ResearchEvidenceItem]) -> int:
    total_weight = sum(item.confidence_score for item in items)
    if total_weight <= 0:
        return round(sum(item.value for item in items) / len(items))

    weighted_total = sum(item.value * item.confidence_score for item in items)
    return round(weighted_total / total_weight)


def score_evidence_items(
    evidence_items: Sequence[ResearchEvidenceItem],
) -> ResearchSignals:
    grouped: dict[str, list[ResearchEvidenceItem]] = {
        key: [] for key in DEFAULT_SIGNAL_SCORES
    }

    for item in evidence_items:
        signal_type = SIGNAL_ALIASES.get(item.signal_type)
        if signal_type is not None:
            grouped[signal_type].append(item)

    scores = {
        signal_type: (
            _weighted_average(items)
            if items
            else DEFAULT_SIGNAL_SCORES[signal_type]
        )
        for signal_type, items in grouped.items()
    }

    return ResearchSignals(
        demand=scores["demand"],
        competition=scores["competition"],
        buyer_intent=scores["buyer_intent"],
        affiliate_potential=scores["affiliate_potential"],
        pinterest_potential=scores["pinterest_potential"],
        seo_potential=scores["seo_potential"],
    )
