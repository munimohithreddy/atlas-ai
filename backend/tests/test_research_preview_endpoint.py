import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.research import preview  # noqa: E402
from app.models.affiliate_program import AffiliateProgram  # noqa: E402
from app.schemas.research import ResearchPreviewRequest  # noqa: E402


class FakeProgramQuery:
    def __init__(self, programs) -> None:
        self.programs = programs

    def order_by(self, *args, **kwargs):
        return self

    def all(self):
        return list(self.programs)


class FakeProgramSession:
    def __init__(self, programs=None) -> None:
        self.programs = programs or []

    def query(self, model):
        return FakeProgramQuery(self.programs)


class ResearchPreviewEndpointTests(unittest.TestCase):
    def test_preview_returns_provider_evidence_without_creating_opportunity(self) -> None:
        response = preview(
            ResearchPreviewRequest(
                topic="best espresso machines",
                niche="coffee",
            ),
            db=FakeProgramSession(),
        )

        self.assertEqual(response["topic"], "best espresso machines")
        self.assertEqual(response["niche"], "coffee")
        self.assertEqual(len(response["evidence"]), 6)
        self.assertEqual(
            {item.signal_type for item in response["evidence"]},
            {
                "demand",
                "competition",
                "buyer_intent",
                "affiliate_potential",
                "pinterest_potential",
                "seo_potential",
            },
        )

    def test_preview_includes_affiliate_evidence_when_program_matches(self) -> None:
        program = AffiliateProgram(
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

        response = preview(
            ResearchPreviewRequest(
                topic="best espresso machines",
                niche="coffee",
            ),
            db=FakeProgramSession(programs=[program]),
        )

        affiliate_evidence = [
            item
            for item in response["evidence"]
            if item.source == "affiliate_programs"
        ]

        self.assertEqual(len(affiliate_evidence), 1)
        self.assertEqual(affiliate_evidence[0].signal_type, "affiliate_potential")


if __name__ == "__main__":
    unittest.main()
