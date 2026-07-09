import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.services.research import MockResearchProvider, ResearchSignals  # noqa: E402


class MockResearchProviderTests(unittest.TestCase):
    def test_research_returns_structured_signals(self) -> None:
        provider = MockResearchProvider()

        signals = provider.research(
            topic="best espresso machines",
            niche="coffee",
        )

        self.assertIsInstance(signals, ResearchSignals)
        self.assertGreaterEqual(signals.demand, 0)
        self.assertLessEqual(signals.demand, 100)
        self.assertGreaterEqual(signals.competition, 0)
        self.assertLessEqual(signals.competition, 100)
        self.assertGreater(signals.buyer_intent, 40)
        self.assertGreater(signals.affiliate_potential, 42)

    def test_research_is_deterministic_for_same_input(self) -> None:
        provider = MockResearchProvider()

        first = provider.research(topic="home office ideas", niche="decor")
        second = provider.research(topic="home office ideas", niche="decor")

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
