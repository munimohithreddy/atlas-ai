import unittest

from pydantic import ValidationError

from bootstrap import configure_test_environment

configure_test_environment()

from app.api.v1.opportunities.routes import portfolio  # noqa: E402
from app.schemas.opportunity import OpportunityPortfolioRequest  # noqa: E402
from app.services.opportunities.portfolio import (  # noqa: E402
    evaluate_opportunity_portfolio,
)
from app.services.research import ResearchOrchestrator  # noqa: E402
from app.services.research.providers import (  # noqa: E402
    EvidenceSignal,
    ResearchProviderResult,
)


class TopicSpecificProvider:
    name = "topic_specific"

    def collect(self, topic: str, niche: str | None = None) -> ResearchProviderResult:
        demand = 90 if "winner" in topic else 40
        evidence = (
            EvidenceSignal(
                source=self.name,
                signal_type="demand",
                value=demand,
                summary=f"Demand evidence for {topic}.",
                confidence_score=90,
            ),
            EvidenceSignal(
                source=self.name,
                signal_type="competition",
                value=30,
                summary=f"Competition evidence for {topic}.",
                confidence_score=80,
            ),
            EvidenceSignal(
                source=self.name,
                signal_type="buyer_intent",
                value=demand,
                summary=f"Buyer intent evidence for {topic}.",
                confidence_score=90,
            ),
            EvidenceSignal(
                source=self.name,
                signal_type="affiliate_potential",
                value=demand,
                summary=f"Affiliate evidence for {topic}.",
                confidence_score=90,
            ),
            EvidenceSignal(
                source=self.name,
                signal_type="pinterest_potential",
                value=50,
                summary=f"Pinterest evidence for {topic}.",
                confidence_score=70,
            ),
            EvidenceSignal(
                source=self.name,
                signal_type="seo_potential",
                value=60,
                summary=f"SEO evidence for {topic}.",
                confidence_score=80,
            ),
        )
        return ResearchProviderResult(provider_name=self.name, evidence=evidence)


class OpportunityPortfolioTests(unittest.TestCase):
    def test_portfolio_endpoint_returns_ranked_results(self) -> None:
        payload = OpportunityPortfolioRequest(
            topics=["best espresso machines", "home office ideas"],
            niche="affiliate",
        )

        response = portfolio(payload=payload)

        self.assertEqual(len(response["results"]), 2)
        self.assertEqual(response["results"][0].rank, 1)
        self.assertGreaterEqual(
            response["results"][0].business_score,
            response["results"][1].business_score,
        )
        self.assertIn(response["results"][0].recommendation, {"BUILD", "WATCH", "SKIP"})
        self.assertGreaterEqual(response["results"][0].confidence, 0)
        self.assertLessEqual(response["results"][0].confidence, 100)

    def test_portfolio_results_are_sorted_by_business_score(self) -> None:
        orchestrator = ResearchOrchestrator(
            providers=(TopicSpecificProvider(),)
        )

        results = evaluate_opportunity_portfolio(
            topics=["steady topic", "winner topic"],
            orchestrator=orchestrator,
        )

        self.assertEqual(results[0].topic, "winner topic")
        self.assertEqual(results[0].rank, 1)
        self.assertGreater(results[0].business_score, results[1].business_score)

    def test_empty_topic_list_is_invalid(self) -> None:
        with self.assertRaises(ValidationError):
            OpportunityPortfolioRequest(topics=[])

    def test_duplicate_topics_are_evaluated_once(self) -> None:
        payload = OpportunityPortfolioRequest(
            topics=[
                "Best Espresso Machines",
                "best espresso machines",
                "home office ideas",
            ]
        )

        self.assertEqual(
            payload.topics,
            ["Best Espresso Machines", "home office ideas"],
        )


if __name__ == "__main__":
    unittest.main()
