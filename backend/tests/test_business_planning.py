import unittest
from types import SimpleNamespace
from unittest.mock import patch

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.business_plans import create_for_opportunity  # noqa: E402
from app.api.v1.opportunities.routes import create_business_plan  # noqa: E402
from app.services.business_planning.acquisition import AcquisitionChannelRecommendationService  # noqa: E402
from app.services.business_planning.effort import EffortEstimationService  # noqa: E402
from app.services.business_planning.monetization import MonetizationRecommendationService  # noqa: E402
from app.services.business_planning.revenue import RevenueEstimationService  # noqa: E402


class FakeBusinessPlanSession:
    def __init__(self) -> None:
        self.created = []
        self.next_id = 1

    def add(self, item) -> None:
        self.created.append(item)

    def commit(self) -> None:
        pass

    def refresh(self, item) -> None:
        if getattr(item, "id", None) is None:
            item.id = self.next_id
            self.next_id += 1

    def query(self, model):
        return self

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return None

    def options(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def offset(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def all(self):
        return list(self.created)


class BusinessPlanningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.opportunity = SimpleNamespace(
            id=1,
            topic="best espresso machines",
            niche="coffee",
            demand_score=80,
            competition_score=30,
            buyer_intent_score=85,
            affiliate_score=78,
            pinterest_score=55,
            seo_score=72,
        )

    def test_monetization_recommendation(self) -> None:
        result = MonetizationRecommendationService().recommend(self.opportunity)
        self.assertEqual(result.primary, "affiliate")
        self.assertTrue(result.summary)

    def test_acquisition_recommendation(self) -> None:
        result = AcquisitionChannelRecommendationService().recommend(self.opportunity)
        self.assertEqual(result.primary, "website_seo")
        self.assertIn("email", result.secondary)

    def test_revenue_estimate_boundaries(self) -> None:
        estimate = RevenueEstimationService().estimate(self.opportunity, "affiliate")
        self.assertLessEqual(estimate.low_monthly, estimate.high_monthly)
        self.assertGreaterEqual(estimate.confidence_score, 25)
        self.assertLessEqual(estimate.confidence_score, 100)

    def test_effort_estimate(self) -> None:
        estimate = EffortEstimationService().estimate(self.opportunity)
        self.assertIn(estimate.effort_level, {"low", "medium", "high"})

    def test_business_plan_creation_without_brand(self) -> None:
        db = FakeBusinessPlanSession()
        with patch(
            "app.api.v1.opportunities.routes.get_opportunity",
            return_value=self.opportunity,
        ):
            plan = create_business_plan(
                opportunity_id=1,
                payload=SimpleNamespace(
                    brand_id=None,
                    brand_name=None,
                    user_constraints=None,
                ),
                db=db,
            )
        self.assertEqual(plan.opportunity_id, 1)
        self.assertIsNone(plan.brand_id)

    def test_business_plan_creation_endpoint_missing_opportunity(self) -> None:
        db = FakeBusinessPlanSession()
        with self.assertRaises(Exception):
            create_for_opportunity(
                opportunity_id=1,
                payload=SimpleNamespace(
                    brand_id=None,
                    brand_name=None,
                    user_constraints=None,
                ),
                db=db,
            )

    def test_business_plan_creation_endpoint_success(self) -> None:
        db = FakeBusinessPlanSession()
        with patch("app.api.v1.business_plans.get_opportunity", return_value=self.opportunity):
            plan = create_for_opportunity(
                opportunity_id=1,
                payload=SimpleNamespace(
                    brand_id=None,
                    brand_name="WorkspaceHQ",
                    user_constraints=None,
                ),
                db=db,
            )

        self.assertEqual(plan.opportunity_id, 1)
        self.assertEqual(plan.brand_id, 1)


if __name__ == "__main__":
    unittest.main()
