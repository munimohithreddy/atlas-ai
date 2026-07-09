from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class EvidenceSignal:
    source: str
    signal_type: str
    value: int
    summary: str
    confidence_score: int


@dataclass(frozen=True)
class ResearchProviderResult:
    provider_name: str
    evidence: tuple[EvidenceSignal, ...]


@runtime_checkable
class ResearchProvider(Protocol):
    name: str

    def collect(self, topic: str, niche: str | None = None) -> ResearchProviderResult:
        pass
