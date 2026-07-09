import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.models.affiliate_program import AffiliateProgram  # noqa: E402
from app.services.affiliate_intelligence import (  # noqa: E402
    estimate_affiliate_potential,
    find_matching_affiliate_programs,
)


class AffiliateIntelligenceTests(unittest.TestCase):
    def test_estimates_affiliate_potential_for_matching_programs(self) -> None:
        programs = [
            AffiliateProgram(
                name="Coffee Gear Partner",
                network="Impact",
                category="coffee",
                website_url="https://example.com/coffee",
                commission_type="percent",
                commission_rate=12.5,
                cookie_duration_days=30,
                approval_required=False,
                notes="espresso machines",
            )
        ]

        score = estimate_affiliate_potential(
            topic="best espresso machines",
            niche="coffee",
            programs=programs,
        )

        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)

    def test_finds_matching_programs_by_category_or_notes(self) -> None:
        programs = [
            AffiliateProgram(
                name="Coffee Gear Partner",
                network="Impact",
                category="coffee",
                website_url="https://example.com/coffee",
                commission_type="percent",
                commission_rate=12.5,
                cookie_duration_days=30,
                approval_required=True,
                notes="espresso machines",
            )
        ]

        matches = find_matching_affiliate_programs(
            topic="best espresso machines",
            niche=None,
            programs=programs,
        )

        self.assertEqual(len(matches), 1)


if __name__ == "__main__":
    unittest.main()
