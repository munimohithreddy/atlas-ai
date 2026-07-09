def calculate_opportunity_score(
    demand_score: int,
    competition_score: int,
    buyer_intent_score: int,
    affiliate_score: int,
    pinterest_score: int,
    seo_score: int,
) -> float:
    score = (
        demand_score * 0.25
        + buyer_intent_score * 0.25
        + affiliate_score * 0.20
        + pinterest_score * 0.10
        + seo_score * 0.15
        + (100 - competition_score) * 0.05
    )
    return round(score, 2)


def make_recommendation(score: float) -> str:
    if score >= 75:
        return "BUILD"
    if score >= 55:
        return "WATCH"
    return "SKIP"


def build_reasoning(
    topic: str,
    score: float,
    recommendation: str,
    demand_score: int,
    competition_score: int,
    buyer_intent_score: int,
    affiliate_score: int,
    pinterest_score: int,
    seo_score: int,
) -> str:
    return (
        f"{topic} scored {score}/100 with recommendation {recommendation}. "
        f"Demand={demand_score}, Competition={competition_score}, "
        f"BuyerIntent={buyer_intent_score}, Affiliate={affiliate_score}, "
        f"Pinterest={pinterest_score}, SEO={seo_score}."
    )
