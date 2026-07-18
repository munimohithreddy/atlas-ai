from sqlalchemy.orm import Session, selectinload

from app.models.campaign import Campaign


def create_campaign(db: Session, campaign: Campaign) -> Campaign:
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def get_campaign(db: Session, campaign_id: int) -> Campaign | None:
    return (
        db.query(Campaign)
        .options(selectinload(Campaign.tasks), selectinload(Campaign.assets), selectinload(Campaign.business_plan))
        .filter(Campaign.id == campaign_id)
        .first()
    )


def get_campaign_by_slug(db: Session, slug: str) -> Campaign | None:
    return db.query(Campaign).filter(Campaign.slug == slug).first()


def list_campaigns(db: Session, offset: int = 0, limit: int = 20) -> list[Campaign]:
    return (
        db.query(Campaign)
        .options(selectinload(Campaign.tasks), selectinload(Campaign.assets))
        .order_by(Campaign.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def update_campaign(db: Session, campaign: Campaign) -> Campaign:
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign
