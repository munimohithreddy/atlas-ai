from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchEvidenceItem:
    source: str
    signal_type: str
    value: int
    summary: str
    confidence_score: int


@dataclass(frozen=True)
class ResearchSignals:
    demand: int
    competition: int
    buyer_intent: int
    affiliate_potential: int
    pinterest_potential: int
    seo_potential: int


@dataclass(frozen=True)
class ResearchResult:
    signals: ResearchSignals
    evidence: tuple[ResearchEvidenceItem, ...]
