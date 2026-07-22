def humanize_enum(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(part for part in value.replace("-", "_").split("_") if part).title()


def monetization_label(value: str | None) -> str:
    labels = {
        "affiliate": "Affiliate",
        "display_ads": "Display Advertising",
        "digital_product": "Digital Product",
        "lead_generation": "Lead Generation",
        "micro_saas": "Micro SaaS",
        "newsletter_sponsorships": "Newsletter Sponsorships",
    }
    return labels.get(value or "", humanize_enum(value))


def opportunity_campaign_topic(topic: str) -> str:
    words = [word for word in topic.replace("-", " ").split() if word]
    if len(words) > 3:
        words = words[:3]
    return " ".join(words).title()


def campaign_name_for_plan(business_plan) -> str:
    topic = opportunity_campaign_topic(business_plan.opportunity.topic)
    monetization = monetization_label(business_plan.primary_monetization)
    return f"{topic} {monetization} Campaign"
