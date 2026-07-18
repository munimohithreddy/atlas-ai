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
