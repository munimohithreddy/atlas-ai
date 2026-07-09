import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.integrations.search import ManualEvidenceSearchProvider  # noqa: E402
from app.services.research.evidence_scoring import score_evidence_items  # noqa: E402
from app.services.research.signals import ResearchEvidenceItem  # noqa: E402


class ManualEvidenceProviderTests(unittest.TestCase):
    def test_provider_returns_scores_from_submitted_evidence(self) -> None:
        provider = ManualEvidenceSearchProvider()
        evidence = (
            ResearchEvidenceItem(
                source="manual_search",
                signal_type="demand",
                value=80,
                summary="Search volume appears strong.",
                confidence_score=90,
            ),
            ResearchEvidenceItem(
                source="manual_search",
                signal_type="demand",
                value=60,
                summary="Secondary source is more conservative.",
                confidence_score=30,
            ),
            ResearchEvidenceItem(
                source="manual_search",
                signal_type="competition",
                value=45,
                summary="Competition looks manageable.",
                confidence_score=80,
            ),
        )

        result = provider.research(
            topic="best espresso machines",
            niche="coffee",
            evidence_items=evidence,
        )

        self.assertEqual(result.signals.demand, 75)
        self.assertEqual(result.signals.competition, 45)
        self.assertEqual(result.signals.buyer_intent, 50)
        self.assertEqual(result.evidence, evidence)

    def test_score_evidence_items_accepts_signal_aliases(self) -> None:
        signals = score_evidence_items(
            (
                ResearchEvidenceItem(
                    source="manual_search",
                    signal_type="affiliate",
                    value=72,
                    summary="Affiliate programs are available.",
                    confidence_score=80,
                ),
                ResearchEvidenceItem(
                    source="manual_search",
                    signal_type="seo",
                    value=64,
                    summary="SERP looks accessible.",
                    confidence_score=70,
                ),
            )
        )

        self.assertEqual(signals.affiliate_potential, 72)
        self.assertEqual(signals.seo_potential, 64)


if __name__ == "__main__":
    unittest.main()
