from collections.abc import Sequence

from app.services.research.evidence_scoring import score_evidence_items
from app.services.research.signals import ResearchEvidenceItem, ResearchResult


class ManualEvidenceSearchProvider:
    def research(
        self,
        topic: str,
        niche: str | None,
        evidence_items: Sequence[ResearchEvidenceItem],
    ) -> ResearchResult:
        signals = score_evidence_items(evidence_items)
        return ResearchResult(signals=signals, evidence=tuple(evidence_items))
