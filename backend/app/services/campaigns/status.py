from datetime import datetime, timezone


class CampaignStatusService:
    allowed_transitions = {
        "planning": {"approved", "paused", "archived"},
        "approved": {"building", "paused", "archived"},
        "building": {"ready", "paused", "archived"},
        "ready": {"published", "paused", "archived"},
        "published": {"optimizing", "paused", "archived"},
        "optimizing": {"paused", "archived"},
        "paused": {"approved", "building", "archived"},
        "archived": set(),
    }

    active_states = {"planning", "approved", "building", "ready", "published", "optimizing"}

    def transition(self, campaign, new_status: str) -> None:
        current = campaign.status
        if new_status not in self.allowed_transitions.get(current, set()):
            raise ValueError(f"Invalid campaign status transition from {current} to {new_status}")
        campaign.status = new_status
        if new_status == "approved" and campaign.approved_at is None:
            campaign.approved_at = datetime.now(timezone.utc)
