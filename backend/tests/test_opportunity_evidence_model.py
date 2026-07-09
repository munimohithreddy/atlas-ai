import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.models.opportunity_evidence import OpportunityEvidence  # noqa: E402


class OpportunityEvidenceModelTests(unittest.TestCase):
    def test_evidence_model_creation(self) -> None:
        evidence = OpportunityEvidence(
            opportunity_id=1,
            source="mock_research",
            signal_type="demand",
            value=65,
            summary="Mock demand evidence.",
            confidence_score=70,
        )

        self.assertEqual(evidence.opportunity_id, 1)
        self.assertEqual(evidence.source, "mock_research")
        self.assertEqual(evidence.signal_type, "demand")
        self.assertEqual(evidence.value, 65)
        self.assertEqual(evidence.confidence_score, 70)


if __name__ == "__main__":
    unittest.main()
