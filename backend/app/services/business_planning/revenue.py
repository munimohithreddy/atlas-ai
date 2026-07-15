from dataclasses import dataclass


@dataclass(frozen=True)
class RevenueEstimate:
    low_monthly: int
    high_monthly: int
    confidence_score: int


class RevenueEstimationService:
    def estimate(self, opportunity, primary_monetization: str) -> RevenueEstimate:
        base = max(opportunity.demand_score, opportunity.buyer_intent_score)
        modifier = {
            "affiliate": 1.0,
            "display_ads": 0.8,
            "digital_product": 1.2,
            "lead_generation": 1.1,
            "micro_saas": 1.4,
            "sponsorship": 0.9,
        }.get(primary_monetization, 1.0)
        low = int(round(base * modifier * 10))
        high = int(round(low * 1.75))
        confidence = min(100, max(25, round((opportunity.buyer_intent_score + opportunity.seo_score) / 2)))
        return RevenueEstimate(low_monthly=low, high_monthly=high, confidence_score=confidence)
