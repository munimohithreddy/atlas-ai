import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.services.research import (  # noqa: E402
    ManualEvidenceProvider,
    MockResearchProvider,
    ResearchOrchestrator,
    ResearchProvider,
)
from app.services.research.providers import EvidenceSignal  # noqa: E402
from app.services.research.signals import ResearchEvidenceItem  # noqa: E402


class ResearchProviderArchitectureTests(unittest.TestCase):
    def test_mock_provider_matches_research_provider_protocol(self) -> None:
        provider = MockResearchProvider()

        self.assertIsInstance(provider, ResearchProvider)

    def test_mock_provider_collects_evidence_signals(self) -> None:
        provider = MockResearchProvider()

        result = provider.collect(topic="best espresso machines", niche="coffee")

        self.assertEqual(result.provider_name, "mock_research")
        self.assertEqual(len(result.evidence), 6)
        self.assertTrue(all(isinstance(item, EvidenceSignal) for item in result.evidence))

    def test_manual_provider_collects_submitted_evidence(self) -> None:
        submitted = (
            ResearchEvidenceItem(
                source="manual_search",
                signal_type="demand",
                value=80,
                summary="Search demand appears strong.",
                confidence_score=90,
            ),
        )
        provider = ManualEvidenceProvider(evidence_items=submitted)

        result = provider.collect(topic="best espresso machines", niche="coffee")

        self.assertEqual(result.provider_name, "manual_evidence")
        self.assertEqual(len(result.evidence), 1)
        self.assertEqual(result.evidence[0].source, "manual_search")

    def test_orchestrator_runs_multiple_providers(self) -> None:
        manual_provider = ManualEvidenceProvider(
            evidence_items=(
                ResearchEvidenceItem(
                    source="manual_search",
                    signal_type="demand",
                    value=80,
                    summary="Search demand appears strong.",
                    confidence_score=90,
                ),
            )
        )
        orchestrator = ResearchOrchestrator(
            providers=(MockResearchProvider(), manual_provider)
        )

        evidence = orchestrator.collect_evidence(
            topic="best espresso machines",
            niche="coffee",
        )

        self.assertEqual(len(evidence), 7)
        self.assertIn("manual_search", {item.source for item in evidence})
        self.assertIn("mock_research", {item.source for item in evidence})


if __name__ == "__main__":
    unittest.main()
