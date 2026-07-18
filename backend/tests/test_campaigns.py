import unittest
from types import SimpleNamespace
from unittest.mock import patch

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.campaigns import approve, change_status, create, get_assets, get_by_id, get_tasks, list_all  # noqa: E402
from app.schemas.campaign import CampaignCreate  # noqa: E402
from app.services.campaigns.assets import CampaignAssetPlanner  # noqa: E402
from app.services.campaigns.service import CampaignService  # noqa: E402
from app.services.campaigns.status import CampaignStatusService  # noqa: E402
from app.services.campaigns.tasks import CampaignTaskGenerator  # noqa: E402


class FakeQuery:
    def __init__(self, items):
        self.items = items
        self.campaign_id = None
        self.slug = None

    def options(self, *args, **kwargs):
        return self

    def filter(self, condition):
        column_name = getattr(condition.left, "name", None)
        value = getattr(condition.right, "value", None)
        if column_name == "id":
            self.campaign_id = value
        elif column_name == "slug":
            self.slug = value
        elif column_name == "campaign_id":
            self.campaign_id = value
        return self

    def order_by(self, *args, **kwargs):
        return self

    def offset(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def first(self):
        if self.campaign_id is not None:
            for item in self.items:
                if item.id == self.campaign_id:
                    return item
            return None
        if self.slug is not None:
            for item in self.items:
                if item.slug == self.slug:
                    return item
            return None
        return self.items[0] if self.items else None

    def all(self):
        return list(self.items)


class FakeCampaignSession:
    def __init__(self, business_plan=None):
        self.business_plan = business_plan
        self.campaigns = []
        self.tasks = []
        self.assets = []
        self.next_id = 1

    def add(self, item) -> None:
        if item.__class__.__name__ == "Campaign":
            self.campaigns.append(item)
        elif item.__class__.__name__ == "CampaignTask":
            self.tasks.append(item)
        elif item.__class__.__name__ == "CampaignAsset":
            self.assets.append(item)

    def commit(self) -> None:
        pass

    def flush(self) -> None:
        for item in self.campaigns + self.tasks + self.assets:
            if getattr(item, "id", None) is None:
                item.id = self.next_id
                self.next_id += 1

    def refresh(self, item) -> None:
        if getattr(item, "id", None) is None:
            item.id = self.next_id
            self.next_id += 1

    def query(self, model):
        if model.__name__ == "BusinessPlan":
            return FakeQuery([self.business_plan] if self.business_plan else [])
        if model.__name__ == "Campaign":
            return FakeQuery(self.campaigns)
        if model.__name__ == "CampaignTask":
            return FakeQuery(self.tasks)
        if model.__name__ == "CampaignAsset":
            return FakeQuery(self.assets)
        return FakeQuery([])


class CampaignTests(unittest.TestCase):
    def setUp(self) -> None:
        self.business_plan = SimpleNamespace(
            id=1,
            opportunity_id=10,
            brand_id=20,
            next_action="Validate the brand positioning and approve the campaign brief before launch.",
            revenue_low_monthly=800,
            revenue_high_monthly=1400,
            effort_level="medium",
            recommended_assets=["website", "email_capture", "downloadable_resource"],
            primary_monetization="affiliate",
            primary_acquisition_channel="website_seo",
            opportunity=SimpleNamespace(topic="best espresso machines"),
            brand=SimpleNamespace(id=20, name="WorkspaceHQ"),
            campaign=None,
        )

    def test_campaign_creation(self) -> None:
        db = FakeCampaignSession(self.business_plan)
        campaign = CampaignService().create_campaign(
            db=db,
            business_plan_id=1,
            goal=None,
            priority=None,
            launch_target_date=None,
        )
        self.assertEqual(campaign.business_plan_id, 1)
        self.assertEqual(campaign.expected_monthly_revenue, 1100)
        self.assertGreater(campaign.estimated_build_hours, 0)

    def test_missing_business_plan_returns_404(self) -> None:
        db = FakeCampaignSession(None)
        with self.assertRaises(LookupError):
            CampaignService().create_campaign(db=db, business_plan_id=1, goal=None, priority=None, launch_target_date=None)

    def test_duplicate_campaign_prevention(self) -> None:
        existing = SimpleNamespace(id=2, slug="best-espresso-machines-affiliate-campaign")
        self.business_plan.campaign = existing
        db = FakeCampaignSession(self.business_plan)
        with self.assertRaises(ValueError):
            CampaignService().create_campaign(db=db, business_plan_id=1, goal=None, priority=None, launch_target_date=None)

    def test_expected_revenue_and_build_hours(self) -> None:
        db = FakeCampaignSession(self.business_plan)
        campaign = CampaignService().create_campaign(
            db=db,
            business_plan_id=1,
            goal=None,
            priority=None,
            launch_target_date=None,
        )
        self.assertEqual(campaign.expected_monthly_revenue, 1100)
        self.assertEqual(campaign.estimated_build_hours, 37)

    def test_deterministic_task_generation(self) -> None:
        campaign = SimpleNamespace(id=1)
        tasks = CampaignTaskGenerator().generate(campaign, self.business_plan)
        self.assertEqual(tasks[0].title, "Review and approve campaign objective")
        self.assertEqual(tasks[-1].title, "Launch campaign")
        self.assertTrue(any(task.category == "website" for task in tasks))

    def test_deterministic_asset_planning(self) -> None:
        campaign = SimpleNamespace(id=1)
        assets = CampaignAssetPlanner().plan(campaign, self.business_plan)
        self.assertTrue(any(asset.asset_type == "website" for asset in assets))
        self.assertTrue(any(asset.asset_type == "email_capture" for asset in assets))

    def test_campaign_status_transition_valid(self) -> None:
        campaign = SimpleNamespace(status="planning", approved_at=None)
        CampaignStatusService().transition(campaign, "approved")
        self.assertEqual(campaign.status, "approved")
        self.assertIsNotNone(campaign.approved_at)

    def test_campaign_status_transition_invalid(self) -> None:
        campaign = SimpleNamespace(status="ready", approved_at=None)
        with self.assertRaises(ValueError):
            CampaignStatusService().transition(campaign, "planning")

    def test_campaign_approval_route(self) -> None:
        campaign = SimpleNamespace(
            id=1,
            status="planning",
            approved_at=None,
            tasks=[],
            assets=[],
        )
        with patch("app.api.v1.campaigns.get_campaign", return_value=campaign), patch(
            "app.api.v1.campaigns.update_campaign",
            return_value=campaign,
        ):
            result = approve(campaign_id=1, db=object())
        self.assertEqual(result.status, "approved")

    def test_unique_slug_behavior(self) -> None:
        db = FakeCampaignSession(self.business_plan)
        service = CampaignService()
        campaign = service.create_campaign(db=db, business_plan_id=1, goal=None, priority=None, launch_target_date=None)
        self.business_plan.campaign = campaign
        with self.assertRaises(ValueError):
            service.create_campaign(db=db, business_plan_id=1, goal=None, priority=None, launch_target_date=None)


if __name__ == "__main__":
    unittest.main()
