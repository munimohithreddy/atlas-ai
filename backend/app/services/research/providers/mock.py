from app.services.research.evidence_scoring import score_evidence_items
from app.services.research.providers.base import EvidenceSignal, ResearchProviderResult
from app.services.research.signals import ResearchEvidenceItem, ResearchResult


COMMERCIAL_TERMS = {
    "best",
    "buy",
    "cheap",
    "comparison",
    "review",
    "reviews",
    "software",
    "tools",
    "vs",
}

VISUAL_TERMS = {
    "decor",
    "design",
    "fashion",
    "garden",
    "home",
    "ideas",
    "kitchen",
    "travel",
}

MOCK_SOURCE = "mock_research"


def _clamp_score(value: int) -> int:
    return max(0, min(100, value))


def _evidence(signal_type: str, value: int, summary: str) -> EvidenceSignal:
    return EvidenceSignal(
        source=MOCK_SOURCE,
        signal_type=signal_type,
        value=value,
        summary=summary,
        confidence_score=70,
    )


class MockResearchProvider:
    name = "mock_research"

    def collect(self, topic: str, niche: str | None = None) -> ResearchProviderResult:
        topic_words = topic.lower().split()
        combined_text = f"{topic} {niche or ''}".lower()

        commercial_matches = sum(term in topic_words for term in COMMERCIAL_TERMS)
        visual_matches = sum(term in combined_text for term in VISUAL_TERMS)
        word_count = len(topic_words)

        demand = _clamp_score(45 + min(word_count * 4, 20) + (8 if niche else 0))
        competition = _clamp_score(
            35 + min(word_count * 5, 25) + commercial_matches * 7
        )
        buyer_intent = _clamp_score(
            40 + commercial_matches * 18 + (8 if "for" in topic_words else 0)
        )
        affiliate_potential = _clamp_score(
            42 + commercial_matches * 15 + (10 if niche else 0)
        )
        pinterest_potential = _clamp_score(
            35 + visual_matches * 14 + min(word_count * 3, 12)
        )
        seo_potential = _clamp_score(
            48 + min(word_count * 4, 18) - commercial_matches * 3
        )

        evidence = (
            _evidence(
                "demand",
                demand,
                f"Mock demand estimate from topic length and niche context for '{topic}'.",
            ),
            _evidence(
                "competition",
                competition,
                f"Mock competition estimate from topic breadth and commercial modifiers for '{topic}'.",
            ),
            _evidence(
                "buyer_intent",
                buyer_intent,
                f"Mock buyer intent estimate from commercial wording in '{topic}'.",
            ),
            _evidence(
                "affiliate_potential",
                affiliate_potential,
                f"Mock affiliate estimate from commercial wording and niche context for '{topic}'.",
            ),
            _evidence(
                "pinterest_potential",
                pinterest_potential,
                f"Mock Pinterest estimate from visual topic terms in '{topic}'.",
            ),
            _evidence(
                "seo_potential",
                seo_potential,
                f"Mock SEO estimate from topic specificity and commercial competition for '{topic}'.",
            ),
        )

        return ResearchProviderResult(provider_name=self.name, evidence=evidence)

    def research(self, topic: str, niche: str | None = None) -> ResearchResult:
        result = self.collect(topic=topic, niche=niche)
        evidence_items = tuple(
            ResearchEvidenceItem(
                source=item.source,
                signal_type=item.signal_type,
                value=item.value,
                summary=item.summary,
                confidence_score=item.confidence_score,
            )
            for item in result.evidence
        )
        return ResearchResult(
            signals=score_evidence_items(evidence_items),
            evidence=evidence_items,
        )
