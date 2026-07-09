from collections.abc import Sequence

from app.services.research.evidence_scoring import score_evidence_items
from app.services.research.providers import (
    EvidenceSignal,
    MockResearchProvider,
    ResearchProvider,
)
from app.services.research.signals import ResearchEvidenceItem, ResearchResult


class ResearchOrchestrator:
    def __init__(self, providers: Sequence[ResearchProvider] | None = None) -> None:
        self.providers = tuple(providers or (MockResearchProvider(),))

    def collect_evidence(
        self,
        topic: str,
        niche: str | None = None,
    ) -> tuple[EvidenceSignal, ...]:
        evidence: list[EvidenceSignal] = []
        for provider in self.providers:
            result = provider.collect(topic=topic, niche=niche)
            evidence.extend(result.evidence)
        return tuple(evidence)

    def research(self, topic: str, niche: str | None = None) -> ResearchResult:
        evidence = self.collect_evidence(topic=topic, niche=niche)
        evidence_items = tuple(
            ResearchEvidenceItem(
                source=item.source,
                signal_type=item.signal_type,
                value=item.value,
                summary=item.summary,
                confidence_score=item.confidence_score,
            )
            for item in evidence
        )
        return ResearchResult(
            signals=score_evidence_items(evidence_items),
            evidence=evidence_items,
        )
