import unittest

from bootstrap import configure_test_environment

configure_test_environment()

from app.schemas.opportunity import OpportunityEvidenceCreate  # noqa: E402
from app.services.opportunities.evidence_scoring import (  # noqa: E402
    NEUTRAL_DEFAULT_SCORE,
    calculate_scores_from_evidence,
)


class EvidenceBasedScoringTests(unittest.TestCase):
    def test_single_evidence_item_scoring(self) -> None:
        scores = calculate_scores_from_evidence(
            (
                OpportunityEvidenceCreate(
                    source="manual_search",
                    signal_type="demand",
                    value=80,
                    summary="Search demand appears strong.",
                    confidence_score=90,
                ),
            )
        )

        self.assertEqual(scores.demand_score, 80)

    def test_multiple_evidence_items_use_confidence_weighted_average(self) -> None:
        scores = calculate_scores_from_evidence(
            (
                OpportunityEvidenceCreate(
                    source="manual_search",
                    signal_type="demand",
                    value=80,
                    summary="High-confidence demand evidence.",
                    confidence_score=90,
                ),
                OpportunityEvidenceCreate(
                    source="manual_search",
                    signal_type="demand",
                    value=60,
                    summary="Lower-confidence demand evidence.",
                    confidence_score=30,
                ),
            )
        )

        self.assertEqual(scores.demand_score, 75)

    def test_missing_signals_default_to_neutral_score(self) -> None:
        scores = calculate_scores_from_evidence(())

        self.assertEqual(scores.demand_score, NEUTRAL_DEFAULT_SCORE)
        self.assertEqual(scores.competition_score, NEUTRAL_DEFAULT_SCORE)
        self.assertEqual(scores.buyer_intent_score, NEUTRAL_DEFAULT_SCORE)
        self.assertEqual(scores.affiliate_score, NEUTRAL_DEFAULT_SCORE)
        self.assertEqual(scores.pinterest_score, NEUTRAL_DEFAULT_SCORE)
        self.assertEqual(scores.seo_score, NEUTRAL_DEFAULT_SCORE)

    def test_affiliate_potential_maps_to_affiliate_score(self) -> None:
        scores = calculate_scores_from_evidence(
            (
                OpportunityEvidenceCreate(
                    source="affiliate_programs",
                    signal_type="affiliate_potential",
                    value=72,
                    summary="Stored affiliate programs match this niche.",
                    confidence_score=80,
                ),
            )
        )

        self.assertEqual(scores.affiliate_score, 72)


if __name__ == "__main__":
    unittest.main()
