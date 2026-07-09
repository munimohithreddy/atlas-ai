import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.services.opportunities.scoring import (  # noqa: E402
    build_reasoning,
    calculate_opportunity_score,
    make_recommendation,
)


class OpportunityScoringTests(unittest.TestCase):
    def test_calculate_opportunity_score_uses_weighted_inputs(self) -> None:
        score = calculate_opportunity_score(
            demand_score=80,
            competition_score=40,
            buyer_intent_score=90,
            affiliate_score=70,
            pinterest_score=60,
            seo_score=50,
        )

        self.assertEqual(score, 73.0)

    def test_make_recommendation_uses_score_thresholds(self) -> None:
        self.assertEqual(make_recommendation(75), "BUILD")
        self.assertEqual(make_recommendation(55), "WATCH")
        self.assertEqual(make_recommendation(54.99), "SKIP")

    def test_build_reasoning_includes_scoring_context(self) -> None:
        reasoning = build_reasoning(
            topic="best espresso machines",
            score=73.0,
            recommendation="WATCH",
            demand_score=80,
            competition_score=40,
            buyer_intent_score=90,
            affiliate_score=70,
            pinterest_score=60,
            seo_score=50,
        )

        self.assertIn("best espresso machines scored 73.0/100", reasoning)
        self.assertIn("recommendation WATCH", reasoning)
        self.assertIn("Competition=40", reasoning)


if __name__ == "__main__":
    unittest.main()
