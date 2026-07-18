from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Campaign(Base):
    __tablename__ = "campaigns"
    __table_args__ = (UniqueConstraint("slug", name="uq_campaigns_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    business_plan_id: Mapped[int] = mapped_column(
        ForeignKey("business_plans.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"), nullable=True, index=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="planning")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    expected_monthly_revenue: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_build_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    launch_target_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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

    business_plan: Mapped["BusinessPlan"] = relationship("BusinessPlan", back_populates="campaign")
    brand: Mapped["Brand | None"] = relationship("Brand", back_populates="campaigns")
    opportunity: Mapped["Opportunity"] = relationship("Opportunity", back_populates="campaigns")
    tasks: Mapped[list["CampaignTask"]] = relationship(
        "CampaignTask",
        back_populates="campaign",
        cascade="all, delete-orphan",
        order_by="CampaignTask.order_index",
    )
    assets: Mapped[list["CampaignAsset"]] = relationship(
        "CampaignAsset",
        back_populates="campaign",
        cascade="all, delete-orphan",
    )


from app.models.brand import Brand  # noqa: E402,F401
from app.models.business_plan import BusinessPlan  # noqa: E402,F401
from app.models.opportunity import Opportunity  # noqa: E402,F401
from app.models.campaign_asset import CampaignAsset  # noqa: E402,F401
from app.models.campaign_task import CampaignTask  # noqa: E402,F401
