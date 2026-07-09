from app.services.research.signals import ResearchSignals


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


def _clamp_score(value: int) -> int:
    return max(0, min(100, value))


class MockResearchProvider:
    def research(self, topic: str, niche: str | None = None) -> ResearchSignals:
        topic_words = topic.lower().split()
        combined_text = f"{topic} {niche or ''}".lower()

        commercial_matches = sum(term in topic_words for term in COMMERCIAL_TERMS)
        visual_matches = sum(term in combined_text for term in VISUAL_TERMS)
        word_count = len(topic_words)

        demand = 45 + min(word_count * 4, 20) + (8 if niche else 0)
        competition = 35 + min(word_count * 5, 25) + commercial_matches * 7
        buyer_intent = 40 + commercial_matches * 18 + (8 if "for" in topic_words else 0)
        affiliate_potential = 42 + commercial_matches * 15 + (10 if niche else 0)
        pinterest_potential = 35 + visual_matches * 14 + min(word_count * 3, 12)
        seo_potential = 48 + min(word_count * 4, 18) - commercial_matches * 3

        return ResearchSignals(
            demand=_clamp_score(demand),
            competition=_clamp_score(competition),
            buyer_intent=_clamp_score(buyer_intent),
            affiliate_potential=_clamp_score(affiliate_potential),
            pinterest_potential=_clamp_score(pinterest_potential),
            seo_potential=_clamp_score(seo_potential),
        )
