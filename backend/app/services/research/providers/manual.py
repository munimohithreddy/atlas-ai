from collections.abc import Sequence

from app.services.research.evidence_scoring import score_evidence_items
from app.services.research.providers.base import EvidenceSignal, ResearchProviderResult
from app.services.research.signals import ResearchEvidenceItem, ResearchResult


class ManualEvidenceProvider:
    name = "manual_evidence"

    def __init__(
        self,
        evidence_items: Sequence[ResearchEvidenceItem] | None = None,
    ) -> None:
        self.evidence_items = tuple(evidence_items or ())

    def collect(self, topic: str, niche: str | None = None) -> ResearchProviderResult:
        evidence = tuple(
            EvidenceSignal(
                source=item.source,
                signal_type=item.signal_type,
                value=item.value,
                summary=item.summary,
                confidence_score=item.confidence_score,
            )
            for item in self.evidence_items
        )
        return ResearchProviderResult(provider_name=self.name, evidence=evidence)

    def research(
        self,
        topic: str,
        niche: str | None,
        evidence_items: Sequence[ResearchEvidenceItem] | None = None,
    ) -> ResearchResult:
        items = tuple(evidence_items or self.evidence_items)
        return ResearchResult(
            signals=score_evidence_items(items),
            evidence=items,
        )
