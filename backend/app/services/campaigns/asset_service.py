from __future__ import annotations

from datetime import datetime, timezone

from app.models.campaign_asset import CampaignAsset
from app.repositories.campaign_asset_repository import (
    count_campaign_assets,
    get_campaign_asset,
    list_asset_queue,
    next_asset_order_index,
    update_campaign_asset,
)
from app.repositories.campaign_task_repository import get_campaign_task


class CampaignAssetService:
    def get_asset(self, db, campaign_id: int, asset_id: int) -> CampaignAsset | None:
        return get_campaign_asset(db, campaign_id, asset_id)

    def create_asset(self, db, campaign, payload):
        if payload.campaign_task_id is not None:
            task = get_campaign_task(db, campaign.id, payload.campaign_task_id)
            if task is None:
                raise LookupError("Campaign task not found")
        asset = CampaignAsset(
            campaign_id=campaign.id,
            campaign_task_id=payload.campaign_task_id,
            title=payload.title,
            description=payload.description,
            asset_type=payload.asset_type,
            channel=payload.channel,
            status="planned",
            priority=payload.priority,
            content_brief=payload.content_brief,
            target_audience=payload.target_audience,
            primary_keyword=payload.primary_keyword,
            secondary_keywords=",".join(payload.secondary_keywords) if payload.secondary_keywords else None,
            call_to_action=payload.call_to_action,
            assigned_to=payload.assigned_to,
            estimated_hours=payload.estimated_hours,
            actual_hours=payload.actual_hours,
            due_date=payload.due_date,
            order_index=payload.order_index or next_asset_order_index(db, campaign.id),
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset

    def update_asset(self, db, campaign, asset, payload):
        if payload.campaign_task_id is not None:
            task = get_campaign_task(db, campaign.id, payload.campaign_task_id)
            if task is None:
                raise LookupError("Campaign task not found")
        for field, value in payload.model_dump(exclude_unset=True).items():
            if field == "secondary_keywords" and value is not None:
                value = ",".join(value)
            setattr(asset, field, value)
        return update_campaign_asset(db, asset)

    def list_queue(self, db, **filters):
        return list_asset_queue(db, **filters)

    def counts(self, db, campaign_id: int) -> dict[str, int]:
        return count_campaign_assets(db, campaign_id)

    def transition(self, db, campaign, asset, action: str, reason: str | None = None):
        allowed = {
            "queue": {"planned"},
            "start": {"queued"},
            "block": {"queued", "in_production"},
            "unblock": {"blocked"},
            "submit-for-review": {"in_production"},
            "approve": {"review"},
            "reject": {"review"},
            "resubmit": {"rejected"},
            "mark-ready-to-publish": {"approved"},
            "cancel": {"planned", "queued", "in_production", "review", "rejected"},
            "reopen": {"cancelled"},
        }
        if asset.status not in allowed[action]:
            raise ValueError("Invalid asset transition")
        if action == "block":
            if not reason:
                raise ValueError("Blocked reason is required.")
            asset.blocked_reason = reason
            asset.status = "blocked"
            return update_campaign_asset(db, asset)
        if action == "unblock":
            asset.status = "queued"
            return update_campaign_asset(db, asset)
        if action == "approve":
            asset.status = "approved"
            asset.approved_at = datetime.now(timezone.utc)
            return update_campaign_asset(db, asset)
        if action == "start":
            asset.status = "in_production"
            asset.started_at = asset.started_at or datetime.now(timezone.utc)
        elif action == "submit-for-review":
            asset.status = "review"
        elif action == "reject":
            asset.status = "rejected"
            asset.rejection_reason = reason or asset.review_notes
        elif action == "resubmit":
            asset.status = "in_production"
            asset.rejection_reason = None
        elif action == "mark-ready-to-publish":
            asset.status = "ready_to_publish"
        elif action == "cancel":
            asset.status = "cancelled"
        elif action == "reopen":
            asset.status = "planned"
        elif action == "queue":
            asset.status = "queued"
        return update_campaign_asset(db, asset)
