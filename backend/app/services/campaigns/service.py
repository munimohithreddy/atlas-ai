from datetime import datetime, timezone

from app.models.campaign import Campaign
from app.repositories.business_plan_repository import get_business_plan
from app.repositories.campaign_asset_repository import create_campaign_assets
from app.repositories.campaign_repository import create_campaign, get_campaign_by_slug
from app.repositories.campaign_task_repository import create_campaign_tasks
from app.services.campaigns.assets import CampaignAssetPlanner
from app.services.campaigns.tasks import CampaignTaskGenerator


class CampaignService:
    def __init__(
        self,
        task_generator: CampaignTaskGenerator | None = None,
        asset_planner: CampaignAssetPlanner | None = None,
    ) -> None:
        self.task_generator = task_generator or CampaignTaskGenerator()
        self.asset_planner = asset_planner or CampaignAssetPlanner()

    def create_campaign(self, db, business_plan_id: int, goal: str | None, priority: str | None, launch_target_date):
        business_plan = get_business_plan(db, business_plan_id)
        if business_plan is None:
            raise LookupError("BusinessPlan not found")
        if business_plan.campaign is not None or get_campaign_by_slug(db, self._slug_for_plan(business_plan)) is not None:
            raise ValueError("Campaign already exists for this business plan")

        expected_revenue = round((business_plan.revenue_low_monthly + business_plan.revenue_high_monthly) / 2)
        build_hours = self._estimate_build_hours(business_plan)
        campaign = Campaign(
            business_plan_id=business_plan.id,
            brand_id=business_plan.brand_id,
            opportunity_id=business_plan.opportunity_id,
            name=self._name_for_plan(business_plan),
            slug=self._slug_for_plan(business_plan),
            goal=goal or business_plan.next_action,
            status="planning",
            priority=priority or "medium",
            expected_monthly_revenue=expected_revenue,
            estimated_build_hours=build_hours,
            launch_target_date=launch_target_date,
        )
        create_campaign(db, campaign)
        create_campaign_tasks(db, self.task_generator.generate(campaign, business_plan))
        create_campaign_assets(db, self.asset_planner.plan(campaign, business_plan))
        return campaign

    def _name_for_plan(self, business_plan) -> str:
        return f"{business_plan.primary_monetization.title()} Campaign for {business_plan.opportunity.topic}"

    def _slug_for_plan(self, business_plan) -> str:
        base = f"{business_plan.opportunity.topic}-{business_plan.primary_monetization}-campaign"
        return base.lower().replace(" ", "-").replace("/", "-")

    def _estimate_build_hours(self, business_plan) -> int:
        hours = 18
        if business_plan.effort_level == "medium":
            hours = 28
        elif business_plan.effort_level == "high":
            hours = 40
        hours += len(business_plan.recommended_assets) * 3
        return hours
