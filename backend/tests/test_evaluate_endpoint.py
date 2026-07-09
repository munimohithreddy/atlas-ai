import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.opportunities.routes import evaluate  # noqa: E402
from app.schemas.opportunity import OpportunityEvaluateRequest  # noqa: E402


class FakeSession:
    def __init__(self) -> None:
        self.saved = None
        self.committed = False

    def add(self, opportunity) -> None:
        self.saved = opportunity

    def commit(self) -> None:
        self.committed = True

    def refresh(self, opportunity) -> None:
        opportunity.id = 1


class EvaluateEndpointTests(unittest.TestCase):
    def test_evaluate_accepts_topic_and_niche_then_stores_opportunity(self) -> None:
        db = FakeSession()
        payload = OpportunityEvaluateRequest(
            topic="best espresso machines",
            niche="coffee",
        )

        opportunity = evaluate(payload=payload, db=db)

        self.assertTrue(db.committed)
        self.assertIs(db.saved, opportunity)
        self.assertEqual(opportunity.id, 1)
        self.assertEqual(opportunity.topic, "best espresso machines")
        self.assertEqual(opportunity.niche, "coffee")
        self.assertGreaterEqual(opportunity.demand_score, 0)
        self.assertLessEqual(opportunity.demand_score, 100)
        self.assertGreater(opportunity.opportunity_score, 0)
        self.assertIn(opportunity.recommendation, {"BUILD", "WATCH", "SKIP"})


if __name__ == "__main__":
    unittest.main()
