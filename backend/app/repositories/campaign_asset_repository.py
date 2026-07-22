from sqlalchemy.orm import Session

from app.models.campaign_asset import CampaignAsset


def create_campaign_assets(db: Session, assets: list[CampaignAsset]) -> list[CampaignAsset]:
    for asset in assets:
        db.add(asset)
    db.commit()
    for asset in assets:
        db.refresh(asset)
    return assets


def list_campaign_assets(db: Session, campaign_id: int) -> list[CampaignAsset]:
    return (
        db.query(CampaignAsset)
        .filter(CampaignAsset.campaign_id == campaign_id)
        .order_by(CampaignAsset.id.asc())
        .all()
    )


def get_campaign_asset(db: Session, campaign_id: int, asset_id: int) -> CampaignAsset | None:
    return (
        db.query(CampaignAsset)
        .filter(CampaignAsset.campaign_id == campaign_id, CampaignAsset.id == asset_id)
        .first()
    )


def list_asset_queue(
    db: Session,
    campaign_id: int | None = None,
    status: str | None = None,
    channel: str | None = None,
    asset_type: str | None = None,
    assigned_to: str | None = None,
    priority: str | None = None,
) -> list[CampaignAsset]:
    query = db.query(CampaignAsset)
    if campaign_id is not None:
        query = query.filter(CampaignAsset.campaign_id == campaign_id)
    if status is not None:
        query = query.filter(CampaignAsset.status == status)
    if channel is not None:
        query = query.filter(CampaignAsset.channel == channel)
    if asset_type is not None:
        query = query.filter(CampaignAsset.asset_type == asset_type)
    if assigned_to is not None:
        query = query.filter(CampaignAsset.assigned_to == assigned_to)
    if priority is not None:
        query = query.filter(CampaignAsset.priority == priority)
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    assets = query.all()
    return sorted(
        assets,
        key=lambda asset: (
            priority_order.get(asset.priority, 99),
            asset.due_date or getattr(asset, "created_at"),
            asset.order_index,
            asset.created_at,
        ),
    )


def count_campaign_assets(db: Session, campaign_id: int) -> dict[str, int]:
    assets = list_campaign_assets(db, campaign_id)
    counts = {status: 0 for status in ["planned", "queued", "in_production", "review", "approved", "ready_to_publish", "blocked", "rejected", "cancelled"]}
    for asset in assets:
        counts[asset.status] = counts.get(asset.status, 0) + 1
    counts["total_assets"] = len(assets)
    return counts


def update_campaign_asset(db: Session, asset: CampaignAsset) -> CampaignAsset:
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def next_asset_order_index(db: Session, campaign_id: int) -> int:
    assets = list_campaign_assets(db, campaign_id)
    return (max((asset.order_index for asset in assets), default=0) + 1)
