import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.research import preview  # noqa: E402
from app.schemas.research import ResearchPreviewRequest  # noqa: E402


class ResearchPreviewEndpointTests(unittest.TestCase):
    def test_preview_returns_provider_evidence_without_creating_opportunity(self) -> None:
        response = preview(
            ResearchPreviewRequest(
                topic="best espresso machines",
                niche="coffee",
            )
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


if __name__ == "__main__":
    unittest.main()
