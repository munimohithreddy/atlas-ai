from dataclasses import dataclass


@dataclass(frozen=True)
class AcquisitionChannelRecommendation:
    primary: str
    secondary: list[str]
    summary: str


class AcquisitionChannelRecommendationService:
    def recommend(self, opportunity) -> AcquisitionChannelRecommendation:
        ranked = [
            ("website_seo", opportunity.seo_score),
            ("pinterest", opportunity.pinterest_score),
            ("youtube", opportunity.buyer_intent_score),
            ("email", min(opportunity.demand_score, 85)),
            ("instagram", opportunity.pinterest_score - 5),
            ("linkedin", opportunity.buyer_intent_score - 10),
            ("reddit", opportunity.competition_score),
            ("direct_outreach", opportunity.buyer_intent_score if opportunity.competition_score >= 60 else 40),
        ]
        ranked.sort(key=lambda item: item[1], reverse=True)
        if opportunity.seo_score >= 65:
            ranked = [("website_seo", opportunity.seo_score)] + [
                item for item in ranked if item[0] != "website_seo"
            ]
        elif opportunity.pinterest_score >= 65:
            ranked = [("pinterest", opportunity.pinterest_score)] + [
                item for item in ranked if item[0] != "pinterest"
            ]

        secondary = [channel for channel, score in ranked[1:4] if score >= 55]
        summary_parts = [
            "Website SEO is foundational when SEO is strong.",
            "Pinterest is favored by visual discovery signals.",
            "YouTube is favored when buyer intent and demos matter.",
            "Email is treated as an owned asset whenever demand exists.",
        ]
        return AcquisitionChannelRecommendation(
            primary=ranked[0][0],
            secondary=secondary,
            summary=" ".join(summary_parts),
        )
