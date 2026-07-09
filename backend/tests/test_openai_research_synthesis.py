import json
import unittest
from types import SimpleNamespace

from bootstrap import configure_test_environment

configure_test_environment()

from app.integrations.openai import OpenAIResearchClient  # noqa: E402
from app.schemas.opportunity import OpportunityEvidenceCreate  # noqa: E402
from app.services.research.analysis import (  # noqa: E402
    OpportunityScoreSnapshot,
    build_fallback_analysis,
    synthesize_opportunity_analysis,
)


class FakeResponses:
    def create(self, model: str, input: str):
        return SimpleNamespace(
            output_text=json.dumps(
                {
                    "executive_summary": "Strong coffee affiliate opportunity.",
                    "key_strengths": ["High intent", "Clear affiliate fit"],
                    "key_risks": ["Competitive SERP"],
                    "recommendation_reason": "Evidence supports a WATCH decision.",
                    "suggested_next_actions": ["Validate SERP", "Find programs"],
                }
            )
        )


class FakeOpenAIClient:
    responses = FakeResponses()


class OpenAIResearchSynthesisTests(unittest.TestCase):
    def test_synthesis_uses_mocked_openai_response(self) -> None:
        client = OpenAIResearchClient(
            api_key="test-key",
            model="test-model",
            client=FakeOpenAIClient(),
        )
        evidence = [
            OpportunityEvidenceCreate(
                source="manual_search",
                signal_type="demand",
                value=80,
                summary="Search demand appears strong.",
                confidence_score=90,
            )
        ]
        scores = OpportunityScoreSnapshot(
            demand_score=80,
            competition_score=45,
            buyer_intent_score=85,
            affiliate_score=50,
            pinterest_score=50,
            seo_score=50,
            opportunity_score=68.25,
            recommendation="WATCH",
        )

        analysis = synthesize_opportunity_analysis(
            topic="best espresso machines",
            niche="coffee",
            evidence_items=evidence,
            scores=scores,
            client=client,
        )

        self.assertEqual(
            analysis.executive_summary,
            "Strong coffee affiliate opportunity.",
        )
        self.assertEqual(analysis.key_strengths[0], "High intent")
        self.assertEqual(analysis.suggested_next_actions[1], "Find programs")

    def test_synthesis_falls_back_without_openai_client(self) -> None:
        client = OpenAIResearchClient(api_key=None, model="test-model")
        scores = OpportunityScoreSnapshot(
            demand_score=80,
            competition_score=45,
            buyer_intent_score=85,
            affiliate_score=50,
            pinterest_score=50,
            seo_score=50,
            opportunity_score=68.25,
            recommendation="WATCH",
        )

        analysis = synthesize_opportunity_analysis(
            topic="best espresso machines",
            niche="coffee",
            evidence_items=[],
            scores=scores,
            client=client,
        )

        self.assertEqual(
            analysis,
            build_fallback_analysis(
                topic="best espresso machines",
                niche="coffee",
                scores=scores,
            ),
        )


if __name__ == "__main__":
    unittest.main()
