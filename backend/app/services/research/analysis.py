from dataclasses import dataclass
from collections.abc import Sequence

from app.core.config import settings
from app.integrations.openai import OpenAIResearchClient
from app.schemas.opportunity import OpportunityEvidenceCreate


@dataclass(frozen=True)
class OpportunityScoreSnapshot:
    demand_score: int
    competition_score: int
    buyer_intent_score: int
    affiliate_score: int
    pinterest_score: int
    seo_score: int
    opportunity_score: float
    recommendation: str


@dataclass(frozen=True)
class OpportunityAIAnalysis:
    executive_summary: str
    key_strengths: list[str]
    key_risks: list[str]
    recommendation_reason: str
    suggested_next_actions: list[str]


def build_score_snapshot(opportunity) -> OpportunityScoreSnapshot:
    return OpportunityScoreSnapshot(
        demand_score=opportunity.demand_score,
        competition_score=opportunity.competition_score,
        buyer_intent_score=opportunity.buyer_intent_score,
        affiliate_score=opportunity.affiliate_score,
        pinterest_score=opportunity.pinterest_score,
        seo_score=opportunity.seo_score,
        opportunity_score=opportunity.opportunity_score,
        recommendation=opportunity.recommendation,
    )


def synthesize_opportunity_analysis(
    topic: str,
    niche: str | None,
    evidence_items: Sequence[OpportunityEvidenceCreate],
    scores: OpportunityScoreSnapshot,
    client: OpenAIResearchClient | None = None,
) -> OpportunityAIAnalysis:
    research_client = client or OpenAIResearchClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )
    prompt = _build_prompt(
        topic=topic,
        niche=niche,
        evidence_items=evidence_items,
        scores=scores,
    )
    raw_analysis = research_client.synthesize_json(prompt)
    if raw_analysis is None:
        return build_fallback_analysis(topic=topic, niche=niche, scores=scores)

    return _parse_analysis(raw_analysis) or build_fallback_analysis(
        topic=topic,
        niche=niche,
        scores=scores,
    )


def build_fallback_analysis(
    topic: str,
    niche: str | None,
    scores: OpportunityScoreSnapshot,
) -> OpportunityAIAnalysis:
    niche_text = f" in {niche}" if niche else ""
    strongest_signal = max(
        {
            "demand": scores.demand_score,
            "buyer intent": scores.buyer_intent_score,
            "affiliate potential": scores.affiliate_score,
            "Pinterest potential": scores.pinterest_score,
            "SEO potential": scores.seo_score,
        }.items(),
        key=lambda item: item[1],
    )
    weakest_signal = min(
        {
            "competition": 100 - scores.competition_score,
            "demand": scores.demand_score,
            "buyer intent": scores.buyer_intent_score,
            "affiliate potential": scores.affiliate_score,
            "Pinterest potential": scores.pinterest_score,
            "SEO potential": scores.seo_score,
        }.items(),
        key=lambda item: item[1],
    )

    return OpportunityAIAnalysis(
        executive_summary=(
            f"{topic}{niche_text} scored {scores.opportunity_score}/100 "
            f"with a {scores.recommendation} recommendation."
        ),
        key_strengths=[
            f"Strongest signal: {strongest_signal[0]} at {strongest_signal[1]}/100.",
            f"Buyer intent score: {scores.buyer_intent_score}/100.",
        ],
        key_risks=[
            f"Weakest signal: {weakest_signal[0]} at {weakest_signal[1]}/100.",
            f"Competition score: {scores.competition_score}/100.",
        ],
        recommendation_reason=(
            f"The deterministic analysis recommends {scores.recommendation} "
            f"based on the calculated opportunity score."
        ),
        suggested_next_actions=[
            "Review the stored evidence for signal gaps.",
            "Add higher-confidence evidence for any weak signals.",
            "Compare this opportunity against at least two alternatives.",
        ],
    )


def _build_prompt(
    topic: str,
    niche: str | None,
    evidence_items: Sequence[OpportunityEvidenceCreate],
    scores: OpportunityScoreSnapshot,
) -> str:
    evidence_lines = "\n".join(
        (
            f"- source={item.source}; signal={item.signal_type}; "
            f"value={item.value}; confidence={item.confidence_score}; "
            f"summary={item.summary}"
        )
        for item in evidence_items
    )
    return (
        "Synthesize this opportunity research into JSON only. "
        "Return keys: executive_summary, key_strengths, key_risks, "
        "recommendation_reason, suggested_next_actions. "
        "The list fields must be arrays of short strings.\n\n"
        f"Topic: {topic}\n"
        f"Niche: {niche or 'none'}\n"
        f"Scores: demand={scores.demand_score}, "
        f"competition={scores.competition_score}, "
        f"buyer_intent={scores.buyer_intent_score}, "
        f"affiliate={scores.affiliate_score}, "
        f"pinterest={scores.pinterest_score}, "
        f"seo={scores.seo_score}, "
        f"opportunity={scores.opportunity_score}, "
        f"recommendation={scores.recommendation}\n"
        f"Evidence:\n{evidence_lines}"
    )


def _parse_analysis(raw_analysis: dict) -> OpportunityAIAnalysis | None:
    try:
        executive_summary = str(raw_analysis["executive_summary"])
        key_strengths = _parse_string_list(raw_analysis["key_strengths"])
        key_risks = _parse_string_list(raw_analysis["key_risks"])
        recommendation_reason = str(raw_analysis["recommendation_reason"])
        suggested_next_actions = _parse_string_list(
            raw_analysis["suggested_next_actions"]
        )
    except (KeyError, TypeError, ValueError):
        return None

    return OpportunityAIAnalysis(
        executive_summary=executive_summary,
        key_strengths=key_strengths,
        key_risks=key_risks,
        recommendation_reason=recommendation_reason,
        suggested_next_actions=suggested_next_actions,
    )


def _parse_string_list(value) -> list[str]:
    if not isinstance(value, list):
        raise ValueError("Expected a list")
    return [str(item) for item in value]
