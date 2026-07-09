import unittest
from types import SimpleNamespace
from unittest.mock import patch

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.opportunities.routes import get_by_id  # noqa: E402


class GetOpportunityEndpointTests(unittest.TestCase):
    def test_get_by_id_returns_opportunity_with_evidence(self) -> None:
        opportunity = SimpleNamespace(
            id=1,
            topic="best espresso machines",
            niche="coffee",
            demand_score=65,
            competition_score=57,
            buyer_intent_score=58,
            affiliate_score=67,
            pinterest_score=44,
            seo_score=57,
            opportunity_score=59.25,
            recommendation="WATCH",
            reasoning="Mock reasoning.",
            evidence=[
                SimpleNamespace(
                    id=1,
                    opportunity_id=1,
                    source="mock_research",
                    signal_type="demand",
                    value=65,
                    summary="Mock demand evidence.",
                    confidence_score=70,
                )
            ],
        )

        with patch(
            "app.api.v1.opportunities.routes.get_opportunity",
            return_value=opportunity,
        ):
            result = get_by_id(opportunity_id=1, db=object())

        self.assertEqual(result.id, 1)
        self.assertEqual(len(result.evidence), 1)
        self.assertEqual(result.evidence[0].signal_type, "demand")


if __name__ == "__main__":
    unittest.main()
