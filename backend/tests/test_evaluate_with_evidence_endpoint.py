import unittest

from pydantic import ValidationError

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.opportunities.routes import evaluate_with_evidence  # noqa: E402
from app.models.opportunity_evidence import OpportunityEvidence  # noqa: E402
from app.schemas.opportunity import (  # noqa: E402
    OpportunityEvaluateWithEvidenceRequest,
)
from test_evaluate_endpoint import FakeSession  # noqa: E402


class EvaluateWithEvidenceEndpointTests(unittest.TestCase):
    def test_evaluate_with_evidence_stores_opportunity_and_evidence(self) -> None:
        db = FakeSession()
        payload = OpportunityEvaluateWithEvidenceRequest(
            topic="best espresso machines",
            niche="coffee",
            evidence_items=[
                {
                    "source": "manual_search",
                    "signal_type": "demand",
                    "value": 80,
                    "summary": "Search demand appears strong.",
                    "confidence_score": 90,
                },
                {
                    "source": "manual_search",
                    "signal_type": "competition",
                    "value": 45,
                    "summary": "SERP competition looks manageable.",
                    "confidence_score": 80,
                },
                {
                    "source": "manual_search",
                    "signal_type": "buyer_intent",
                    "value": 85,
                    "summary": "Queries show clear buying language.",
                    "confidence_score": 85,
                },
            ],
        )

        opportunity = evaluate_with_evidence(payload=payload, db=db)
        evidence_rows = [
            item for item in db.saved if isinstance(item, OpportunityEvidence)
        ]

        self.assertEqual(opportunity.demand_score, 80)
        self.assertEqual(opportunity.competition_score, 45)
        self.assertEqual(opportunity.buyer_intent_score, 85)
        self.assertEqual(opportunity.affiliate_score, 50)
        self.assertIsNotNone(opportunity.ai_executive_summary)
        self.assertIsNotNone(opportunity.ai_recommendation_reason)
        self.assertEqual(len(evidence_rows), 3)
        self.assertEqual(len(opportunity.evidence), 3)
        self.assertTrue(
            all(item.opportunity_id == opportunity.id for item in evidence_rows)
        )

    def test_confidence_score_rejects_values_below_zero(self) -> None:
        with self.assertRaises(ValidationError):
            OpportunityEvaluateWithEvidenceRequest(
                topic="best espresso machines",
                evidence_items=[
                    {
                        "source": "manual_search",
                        "signal_type": "demand",
                        "value": 80,
                        "summary": "Search demand appears strong.",
                        "confidence_score": -1,
                    }
                ],
            )

    def test_confidence_score_rejects_values_above_one_hundred(self) -> None:
        with self.assertRaises(ValidationError):
            OpportunityEvaluateWithEvidenceRequest(
                topic="best espresso machines",
                evidence_items=[
                    {
                        "source": "manual_search",
                        "signal_type": "demand",
                        "value": 80,
                        "summary": "Search demand appears strong.",
                        "confidence_score": 101,
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()
