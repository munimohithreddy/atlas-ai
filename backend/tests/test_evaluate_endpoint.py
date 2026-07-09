import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.opportunities.routes import evaluate  # noqa: E402
from app.models.opportunity_evidence import OpportunityEvidence  # noqa: E402
from app.schemas.opportunity import OpportunityEvaluateRequest  # noqa: E402


class FakeSession:
    def __init__(self) -> None:
        self.saved = []
        self.commits = 0
        self.next_id = 1

    def add(self, item) -> None:
        self.saved.append(item)

    def commit(self) -> None:
        self.commits += 1

    def refresh(self, item) -> None:
        if getattr(item, "id", None) is None:
            item.id = self.next_id
            self.next_id += 1


class EvaluateEndpointTests(unittest.TestCase):
    def test_evaluate_accepts_topic_and_niche_then_stores_opportunity(self) -> None:
        db = FakeSession()
        payload = OpportunityEvaluateRequest(
            topic="best espresso machines",
            niche="coffee",
        )

        opportunity = evaluate(payload=payload, db=db)

        self.assertEqual(db.commits, 2)
        self.assertIs(db.saved[0], opportunity)
        self.assertEqual(opportunity.id, 1)
        self.assertEqual(opportunity.topic, "best espresso machines")
        self.assertEqual(opportunity.niche, "coffee")
        self.assertGreaterEqual(opportunity.demand_score, 0)
        self.assertLessEqual(opportunity.demand_score, 100)
        self.assertGreater(opportunity.opportunity_score, 0)
        self.assertIn(opportunity.recommendation, {"BUILD", "WATCH", "SKIP"})

    def test_evaluate_stores_evidence_items(self) -> None:
        db = FakeSession()
        payload = OpportunityEvaluateRequest(topic="best espresso machines")

        opportunity = evaluate(payload=payload, db=db)
        evidence_rows = [
            item for item in db.saved if isinstance(item, OpportunityEvidence)
        ]

        self.assertEqual(len(evidence_rows), 6)
        self.assertEqual(len(opportunity.evidence), 6)
        self.assertTrue(
            all(item.opportunity_id == opportunity.id for item in evidence_rows)
        )
        self.assertEqual(
            {item.signal_type for item in evidence_rows},
            {
                "demand",
                "competition",
                "buyer_intent",
                "affiliate_potential",
                "pinterest_potential",
                "seo_potential",
            },
        )


if __name__ == "__main__":
    unittest.main()
