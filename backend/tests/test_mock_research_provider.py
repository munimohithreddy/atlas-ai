import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.services.research import MockResearchProvider, ResearchResult  # noqa: E402


class MockResearchProviderTests(unittest.TestCase):
    def test_research_returns_structured_signals_and_evidence(self) -> None:
        provider = MockResearchProvider()

        result = provider.research(
            topic="best espresso machines",
            niche="coffee",
        )

        self.assertIsInstance(result, ResearchResult)
        self.assertGreaterEqual(result.signals.demand, 0)
        self.assertLessEqual(result.signals.demand, 100)
        self.assertGreaterEqual(result.signals.competition, 0)
        self.assertLessEqual(result.signals.competition, 100)
        self.assertGreater(result.signals.buyer_intent, 40)
        self.assertGreater(result.signals.affiliate_potential, 42)
        self.assertEqual(len(result.evidence), 6)
        self.assertEqual(
            {item.signal_type for item in result.evidence},
            {
                "demand",
                "competition",
                "buyer_intent",
                "affiliate_potential",
                "pinterest_potential",
                "seo_potential",
            },
        )

    def test_research_is_deterministic_for_same_input(self) -> None:
        provider = MockResearchProvider()

        first = provider.research(topic="home office ideas", niche="decor")
        second = provider.research(topic="home office ideas", niche="decor")

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
