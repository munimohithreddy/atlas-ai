from app.models.business_plan import BusinessPlan
from app.repositories.brand_repository import create_brand, get_brand
from app.repositories.business_plan_repository import create_business_plan
from app.schemas.brand import BrandCreate
from app.schemas.business_plan import BusinessPlanConstraints
from app.services.business_planning.acquisition import AcquisitionChannelRecommendationService
from app.services.business_planning.effort import EffortEstimationService
from app.services.business_planning.monetization import MonetizationRecommendationService
from app.services.business_planning.revenue import RevenueEstimationService


class BusinessPlanService:
    def __init__(
        self,
        monetization_service: MonetizationRecommendationService | None = None,
        acquisition_service: AcquisitionChannelRecommendationService | None = None,
        revenue_service: RevenueEstimationService | None = None,
        effort_service: EffortEstimationService | None = None,
    ) -> None:
        self.monetization_service = monetization_service or MonetizationRecommendationService()
        self.acquisition_service = acquisition_service or AcquisitionChannelRecommendationService()
        self.revenue_service = revenue_service or RevenueEstimationService()
        self.effort_service = effort_service or EffortEstimationService()

    def create_plan(
        self,
        db,
        opportunity,
        brand_id: int | None = None,
        brand_name: str | None = None,
        constraints: BusinessPlanConstraints | None = None,
    ) -> BusinessPlan:
        brand = get_brand(db, brand_id) if brand_id is not None else None
        if brand is None and brand_name:
            slug = brand_name.strip().lower().replace(" ", "-")
            brand = create_brand(
                db,
                BrandCreate(name=brand_name, slug=slug, market=opportunity.niche or "general"),
            )

        monetization = self.monetization_service.recommend(opportunity)
        acquisition = self.acquisition_service.recommend(opportunity)
        revenue = self.revenue_service.estimate(opportunity, monetization.primary)
        effort = self.effort_service.estimate(opportunity)

        if constraints and constraints.target_monthly_revenue:
            revenue = revenue.__class__(
                low_monthly=min(revenue.low_monthly, constraints.target_monthly_revenue),
                high_monthly=max(revenue.high_monthly, constraints.target_monthly_revenue),
                confidence_score=revenue.confidence_score,
            )

        plan = BusinessPlan(
            opportunity_id=opportunity.id,
            brand_id=brand.id if brand else None,
            primary_monetization=monetization.primary,
            secondary_monetization=monetization.secondary,
            primary_acquisition_channel=acquisition.primary,
            secondary_acquisition_channels=acquisition.secondary,
            recommended_assets=self._build_assets(acquisition.primary, acquisition.secondary),
            target_audience=self._build_audience(opportunity),
            value_proposition=self._build_value_proposition(opportunity, monetization.primary),
            revenue_low_monthly=revenue.low_monthly,
            revenue_high_monthly=revenue.high_monthly,
            revenue_confidence_score=revenue.confidence_score,
            effort_level=effort.effort_level,
            estimated_launch_days=effort.estimated_launch_days,
            recommendation_summary=" ".join(
                [monetization.summary, acquisition.summary, self._build_summary(opportunity)]
            ),
            next_action="Validate the brand positioning and approve the campaign brief before launch.",
            status="draft",
        )
        return create_business_plan(db, plan)

    def _build_assets(self, primary_channel: str, secondary_channels: list[str]) -> list[str]:
        assets = ["website", "buying_guides", "comparison_pages", "email_capture"]
        if primary_channel == "pinterest" or "pinterest" in secondary_channels:
            assets.append("pinterest_pins")
        if primary_channel == "youtube" or "youtube" in secondary_channels:
            assets.append("youtube_shorts")
        assets.append("downloadable_resource")
        return assets

    def _build_audience(self, opportunity) -> str:
        return f"People searching for {opportunity.topic} in {opportunity.niche or 'the target market'}."

    def _build_value_proposition(self, opportunity, primary_monetization: str) -> str:
        return f"Help the audience evaluate {opportunity.topic} with a {primary_monetization}-first offer."

    def _build_summary(self, opportunity) -> str:
        return "Business planning is deterministic in v1 and keeps monetization separate from acquisition."
