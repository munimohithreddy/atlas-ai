from dataclasses import dataclass


@dataclass(frozen=True)
class EffortEstimate:
    effort_level: str
    estimated_launch_days: int


class EffortEstimationService:
    def estimate(self, opportunity) -> EffortEstimate:
        if opportunity.competition_score >= 70 or opportunity.seo_score >= 70:
            return EffortEstimate(effort_level="high", estimated_launch_days=45)
        if opportunity.buyer_intent_score >= 60 and opportunity.affiliate_score >= 60:
            return EffortEstimate(effort_level="medium", estimated_launch_days=21)
        return EffortEstimate(effort_level="low", estimated_launch_days=14)
