import unittest
from types import SimpleNamespace
from unittest.mock import patch

from pydantic import ValidationError

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.campaigns import approve, change_status, create, get_assets, get_by_id, get_tasks, list_all  # noqa: E402
from app.schemas.campaign import CampaignCreate, CampaignTaskCompleteRequest, CampaignTaskResponse  # noqa: E402
from app.services.campaigns.progress import CampaignProgressService  # noqa: E402
from app.services.campaigns.task_dependencies import CampaignTaskDependencyService  # noqa: E402
from app.services.campaigns.task_service import CampaignTaskService  # noqa: E402
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

    def filter(self, *conditions):
        for condition in conditions:
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
        self.assertEqual(db.tasks[0].status, "pending")
        self.assertEqual(db.tasks[1].status, "pending")

    def test_root_task_becomes_ready_after_approval(self) -> None:
        db = FakeCampaignSession(self.business_plan)
        campaign = CampaignService().create_campaign(
            db=db,
            business_plan_id=1,
            goal=None,
            priority=None,
            launch_target_date=None,
        )
        campaign.status = "approved"
        CampaignService().repair_task_readiness(db, campaign)
        self.assertEqual(db.tasks[0].status, "ready")
        self.assertEqual(db.tasks[1].depends_on_task_id, db.tasks[0].id)

    def test_root_task_becomes_ready_for_existing_building_campaign(self) -> None:
        db = FakeCampaignSession(self.business_plan)
        campaign = CampaignService().create_campaign(
            db=db,
            business_plan_id=1,
            goal=None,
            priority=None,
            launch_target_date=None,
        )
        campaign.status = "building"
        CampaignService().repair_task_readiness(db, campaign)
        self.assertEqual(db.tasks[0].status, "ready")
        self.assertEqual(db.tasks[1].status, "pending")

    def test_repair_readiness_endpoint_repairs_existing_campaign(self) -> None:
        db = FakeCampaignSession(self.business_plan)
        campaign = CampaignService().create_campaign(
            db=db,
            business_plan_id=1,
            goal=None,
            priority=None,
            launch_target_date=None,
        )
        campaign.status = "building"
        with patch("app.api.v1.campaigns.get_campaign", return_value=campaign), patch(
            "app.api.v1.campaigns.update_campaign",
            return_value=campaign,
        ), patch(
            "app.api.v1.campaigns.CampaignProgressService.build_progress",
            return_value={"completion_percentage": 0},
        ):
            from app.api.v1.campaigns import repair_readiness

            result = repair_readiness(campaign_id=campaign.id, db=db)

        self.assertEqual(db.tasks[0].status, "ready")
        self.assertEqual(result.status, "building")

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

    def test_dependency_same_campaign_validation(self) -> None:
        task = SimpleNamespace(depends_on_task_id=99, id=1)
        with self.assertRaises(ValueError):
            CampaignTaskDependencyService().validate(task, [])

    def test_self_dependency_rejection(self) -> None:
        task = SimpleNamespace(depends_on_task_id=1, id=1)
        with self.assertRaises(ValueError):
            CampaignTaskDependencyService().validate(task, [task])

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

    def test_task_start_before_campaign_approval(self) -> None:
        campaign = SimpleNamespace(status="planning")
        task = SimpleNamespace(status="ready", campaign_id=1, depends_on_task_id=None)
        with self.assertRaises(ValueError):
            CampaignTaskService().start(FakeCampaignSession(self.business_plan), campaign, task)

    def test_task_start_moves_approved_campaign_to_building(self) -> None:
        campaign = SimpleNamespace(status="approved", id=1)
        task = SimpleNamespace(status="ready", campaign_id=1, depends_on_task_id=None, started_at=None)
        db = FakeCampaignSession(self.business_plan)
        db.campaigns.append(campaign)
        db.tasks.append(task)
        result = CampaignTaskService().start(db, campaign, task)
        self.assertEqual(campaign.status, "building")
        self.assertEqual(result.status, "in_progress")
        self.assertIsNotNone(result.started_at)

    def test_task_block_and_unblock(self) -> None:
        campaign = SimpleNamespace(status="building", id=1)
        task = SimpleNamespace(status="ready", campaign_id=1, depends_on_task_id=None, blocked_reason=None)
        db = FakeCampaignSession(self.business_plan)
        db.tasks.append(task)
        blocked = CampaignTaskService().block(db, campaign, task, "Waiting on review")
        self.assertEqual(blocked.status, "blocked")
        self.assertEqual(blocked.blocked_reason, "Waiting on review")
        unblocked = CampaignTaskService().unblock(db, campaign, task)
        self.assertEqual(unblocked.status, "ready")

    def test_task_review_flow(self) -> None:
        campaign = SimpleNamespace(status="building", id=1)
        task = SimpleNamespace(status="in_progress", campaign_id=1, depends_on_task_id=None)
        reviewed = CampaignTaskService().review(FakeCampaignSession(self.business_plan), campaign, task)
        self.assertEqual(reviewed.status, "review")

    def test_task_completion_timestamps(self) -> None:
        campaign = SimpleNamespace(status="building", id=1)
        task = SimpleNamespace(status="in_progress", campaign_id=1, depends_on_task_id=None, completed_at=None)
        completed = CampaignTaskService().complete(
            FakeCampaignSession(self.business_plan),
            campaign,
            task,
            completion_notes="done",
            actual_hours=5,
        )
        self.assertEqual(completed.status, "completed")
        self.assertIsNotNone(completed.completed_at)
        self.assertEqual(completed.actual_hours, 5)

    def test_task_completion_accepts_fractional_hours(self) -> None:
        request = CampaignTaskCompleteRequest(completion_notes="done", actual_hours=1.5)
        self.assertEqual(request.actual_hours, 1.5)

    def test_task_completion_accepts_quarter_hour(self) -> None:
        request = CampaignTaskCompleteRequest(completion_notes="done", actual_hours=0.25)
        self.assertEqual(request.actual_hours, 0.25)

    def test_task_completion_accepts_null_hours(self) -> None:
        request = CampaignTaskCompleteRequest(completion_notes="done", actual_hours=None)
        self.assertIsNone(request.actual_hours)

    def test_task_completion_rejects_negative_hours(self) -> None:
        with self.assertRaises(ValidationError):
            CampaignTaskCompleteRequest(completion_notes="done", actual_hours=-0.25)

    def test_task_response_serializes_fractional_hours(self) -> None:
        response = CampaignTaskResponse(
            id=1,
            campaign_id=1,
            title="Task",
            description=None,
            category="content",
            status="completed",
            priority="medium",
            estimated_hours=2,
            started_at=None,
            completed_at=None,
            blocked_reason=None,
            completion_notes="done",
            actual_hours=1.5,
            assigned_to=None,
            due_date=None,
            depends_on_task_id=None,
            order_index=1,
        )
        self.assertEqual(response.actual_hours, 1.5)

    def test_task_completion_persists_fractional_hours(self) -> None:
        campaign = SimpleNamespace(status="building", id=1)
        task = SimpleNamespace(id=1, status="in_progress", campaign_id=1, depends_on_task_id=None, completed_at=None)
        db = FakeCampaignSession(self.business_plan)
        db.tasks.append(task)

        completed = CampaignTaskService().complete(
            db,
            campaign,
            task,
            completion_notes="done",
            actual_hours=2.75,
        )

        self.assertEqual(completed.actual_hours, 2.75)

    def test_task_reopen_moves_ready_campaign_back_to_building(self) -> None:
        campaign = SimpleNamespace(status="ready", id=1)
        task = SimpleNamespace(status="completed", campaign_id=1, depends_on_task_id=None, completed_at=None)
        reopened = CampaignTaskService().reopen(FakeCampaignSession(self.business_plan), campaign, task, "fix")
        self.assertEqual(campaign.status, "building")
        self.assertEqual(reopened.status, "in_progress")

    def test_campaign_progress_calculation(self) -> None:
        db = FakeCampaignSession(self.business_plan)
        campaign = CampaignService().create_campaign(db=db, business_plan_id=1, goal=None, priority=None, launch_target_date=None)
        progress = CampaignProgressService().build_progress(db, campaign)
        self.assertEqual(progress["total_tasks"], len(db.tasks))
        self.assertEqual(progress["blocked_tasks"], 0)
        self.assertGreaterEqual(progress["completion_percentage"], 0)

    def test_task_completion_unlocks_downstream_task(self) -> None:
        campaign = SimpleNamespace(status="building", id=1)
        first = SimpleNamespace(id=1, status="in_progress", campaign_id=1, depends_on_task_id=None, completed_at=None)
        second = SimpleNamespace(id=2, status="pending", campaign_id=1, depends_on_task_id=1)
        db = FakeCampaignSession(self.business_plan)
        db.campaigns.append(campaign)
        db.tasks.extend([first, second])
        completed = CampaignTaskService().complete(db, campaign, first, completion_notes=None, actual_hours=None)
        self.assertEqual(completed.status, "completed")
        self.assertEqual(second.status, "ready")

    def test_cancelled_dependency_unlock_behavior(self) -> None:
        campaign = SimpleNamespace(status="building", id=1)
        first = SimpleNamespace(id=1, status="ready", campaign_id=1, depends_on_task_id=None)
        second = SimpleNamespace(id=2, status="pending", campaign_id=1, depends_on_task_id=1)
        db = FakeCampaignSession(self.business_plan)
        db.tasks.extend([first, second])
        CampaignTaskService().cancel(db, campaign, first)
        self.assertEqual(second.status, "ready")

    def test_archived_and_paused_restrictions(self) -> None:
        archived = SimpleNamespace(status="archived", id=1)
        paused = SimpleNamespace(status="paused", id=1)
        task = SimpleNamespace(status="ready", campaign_id=1, depends_on_task_id=None)
        with self.assertRaises(ValueError):
            CampaignTaskService().start(FakeCampaignSession(self.business_plan), archived, task)
        with self.assertRaises(ValueError):
            CampaignTaskService().start(FakeCampaignSession(self.business_plan), paused, task)

    def test_campaign_approval_route(self) -> None:
        campaign = SimpleNamespace(
            id=1,
            status="planning",
            approved_at=None,
            tasks=[],
            assets=[],
        )
        db = FakeCampaignSession(self.business_plan)
        db.campaigns.append(campaign)
        with patch("app.api.v1.campaigns.get_campaign", return_value=campaign), patch(
            "app.api.v1.campaigns.update_campaign",
            return_value=campaign,
        ), patch(
            "app.api.v1.campaigns.CampaignProgressService.build_progress",
            return_value={"completion_percentage": 0},
        ):
            result = approve(campaign_id=1, db=db)
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
