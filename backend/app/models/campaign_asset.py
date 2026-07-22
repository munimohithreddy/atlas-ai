from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CampaignAsset(Base):
    __tablename__ = "campaign_assets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"), nullable=False, index=True)
    campaign_task_id: Mapped[int | None] = mapped_column(ForeignKey("campaign_tasks.id"), nullable=True, index=True)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    channel: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="planned")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium", index=True)
    content_brief: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_audience: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_keyword: Mapped[str | None] = mapped_column(String(255), nullable=True)
    secondary_keywords: Mapped[str | None] = mapped_column(Text, nullable=True)
    call_to_action: Mapped[str | None] = mapped_column(Text, nullable=True)
    assigned_to: Mapped[str | None] = mapped_column(String(255), nullable=True)
    estimated_hours: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    actual_hours: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    blocked_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    planned_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    generated_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    published_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="assets")
    task: Mapped["CampaignTask | None"] = relationship("CampaignTask")


from app.models.campaign import Campaign  # noqa: E402,F401
from app.models.campaign_task import CampaignTask  # noqa: E402,F401
