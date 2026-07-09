from collections.abc import Sequence
from typing import Protocol

from app.services.research.signals import ResearchEvidenceItem, ResearchResult


class SearchResearchProvider(Protocol):
    def research(
        self,
        topic: str,
        niche: str | None,
        evidence_items: Sequence[ResearchEvidenceItem],
    ) -> ResearchResult:
        pass
