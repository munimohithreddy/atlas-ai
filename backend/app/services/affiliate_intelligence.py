from collections.abc import Sequence

from app.models.affiliate_program import AffiliateProgram


def find_matching_affiliate_programs(
    topic: str,
    niche: str | None,
    programs: Sequence[AffiliateProgram],
) -> list[AffiliateProgram]:
    search_text = f"{topic} {niche or ''}".lower()
    matches = []
    for program in programs:
        terms = {
            program.name.lower(),
            program.category.lower(),
            program.network.lower(),
        }
        if program.notes:
            terms.update(word.lower() for word in program.notes.split())

        if any(term and term in search_text for term in terms):
            matches.append(program)

    return matches


def estimate_affiliate_potential(
    topic: str,
    niche: str | None,
    programs: Sequence[AffiliateProgram],
) -> int:
    matches = find_matching_affiliate_programs(topic=topic, niche=niche, programs=programs)
    if not matches:
        return 0

    best_rate = max(program.commission_rate for program in matches)
    best_cookie = max(program.cookie_duration_days for program in matches)
    approval_bonus = 10 if any(not program.approval_required for program in matches) else 0
    program_depth = min(len(matches) * 10, 30)

    score = 35 + min(round(best_rate), 25) + min(best_cookie // 2, 20)
    return max(0, min(100, score + approval_bonus + program_depth))


def summarize_affiliate_matches(
    topic: str,
    niche: str | None,
    programs: Sequence[AffiliateProgram],
) -> str:
    matches = find_matching_affiliate_programs(topic=topic, niche=niche, programs=programs)
    if not matches:
        return "No matching affiliate programs found."

    names = ", ".join(program.name for program in matches[:3])
    return f"Matched {len(matches)} stored affiliate program(s): {names}."
