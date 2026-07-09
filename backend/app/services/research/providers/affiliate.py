from collections.abc import Sequence

from app.models.affiliate_program import AffiliateProgram
from app.services.affiliate_intelligence import (
    estimate_affiliate_potential,
    find_matching_affiliate_programs,
    summarize_affiliate_matches,
)
from app.services.research.providers.base import EvidenceSignal, ResearchProviderResult


class AffiliateProgramResearchProvider:
    name = "affiliate_programs"

    def __init__(self, programs: Sequence[AffiliateProgram]) -> None:
        self.programs = tuple(programs)

    def collect(self, topic: str, niche: str | None = None) -> ResearchProviderResult:
        matches = find_matching_affiliate_programs(
            topic=topic,
            niche=niche,
            programs=self.programs,
        )
        if not matches:
            return ResearchProviderResult(provider_name=self.name, evidence=())

        score = estimate_affiliate_potential(
            topic=topic,
            niche=niche,
            programs=self.programs,
        )
        evidence = (
            EvidenceSignal(
                source=self.name,
                signal_type="affiliate_potential",
                value=score,
                summary=summarize_affiliate_matches(
                    topic=topic,
                    niche=niche,
                    programs=self.programs,
                ),
                confidence_score=80,
            ),
        )
        return ResearchProviderResult(provider_name=self.name, evidence=evidence)
