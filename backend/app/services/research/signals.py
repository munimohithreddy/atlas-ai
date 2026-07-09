from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchSignals:
    demand: int
    competition: int
    buyer_intent: int
    affiliate_potential: int
    pinterest_potential: int
    seo_potential: int
