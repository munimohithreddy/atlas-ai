from dataclasses import dataclass


@dataclass(frozen=True)
class MonetizationRecommendation:
    primary: str
    secondary: str | None
    summary: str


class MonetizationRecommendationService:
    def recommend(self, opportunity) -> MonetizationRecommendation:
        reasons: list[str] = []
        candidates: list[tuple[str, int]] = [
            ("affiliate", opportunity.affiliate_score),
            ("display_ads", opportunity.seo_score),
            ("digital_product", opportunity.buyer_intent_score),
            ("lead_generation", opportunity.demand_score),
            ("micro_saas", opportunity.competition_score),
            ("sponsorship", opportunity.pinterest_score),
        ]
        if opportunity.affiliate_score >= 70 and opportunity.buyer_intent_score >= 60:
            reasons.append("High affiliate fit with buyer intent favors affiliate monetization.")
        if opportunity.seo_score >= 65 and opportunity.demand_score >= 60:
            reasons.append("Strong SEO and broad demand can support display ads secondarily.")
        if opportunity.buyer_intent_score >= 65:
            reasons.append("Knowledge-heavy topics with clear intent can support digital products.")
        if opportunity.demand_score >= 65:
            reasons.append("Demand-heavy topics can support lead generation offers.")
        if opportunity.competition_score >= 65:
            reasons.append("Repetitive problems in competitive spaces can suggest micro-SaaS.")
        if opportunity.pinterest_score >= 60:
            reasons.append("Visual discovery can support sponsorship packages.")

        ordered = sorted(candidates, key=lambda item: item[1], reverse=True)
        primary = ordered[0][0]
        if opportunity.affiliate_score >= 70 and opportunity.buyer_intent_score >= 60:
            primary = "affiliate"
        elif opportunity.demand_score >= 65 and opportunity.competition_score >= 65:
            primary = "lead_generation"
        elif opportunity.buyer_intent_score >= 65:
            primary = "digital_product"
        elif opportunity.competition_score >= 65:
            primary = "micro_saas"
        secondary = ordered[1][0] if ordered[1][1] >= 55 else None

        if not reasons:
            reasons.append("Selected the highest-scoring monetization fit from the opportunity signals.")

        return MonetizationRecommendation(primary=primary, secondary=secondary, summary=" ".join(reasons))
