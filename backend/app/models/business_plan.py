from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class BusinessPlan(Base):
    __tablename__ = "business_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    brand_id: Mapped[int | None] = mapped_column(
        ForeignKey("brands.id"),
        nullable=True,
        index=True,
    )
    primary_monetization: Mapped[str] = mapped_column(String(50), nullable=False)
    secondary_monetization: Mapped[str | None] = mapped_column(String(50), nullable=True)
    primary_acquisition_channel: Mapped[str] = mapped_column(String(50), nullable=False)
    secondary_acquisition_channels: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    recommended_assets: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    target_audience: Mapped[str] = mapped_column(Text, nullable=False)
    value_proposition: Mapped[str] = mapped_column(Text, nullable=False)
    revenue_low_monthly: Mapped[int] = mapped_column(Integer, nullable=False)
    revenue_high_monthly: Mapped[int] = mapped_column(Integer, nullable=False)
    revenue_confidence_score: Mapped[int] = mapped_column(Integer, nullable=False)
    effort_level: Mapped[str] = mapped_column(String(20), nullable=False)
    estimated_launch_days: Mapped[int] = mapped_column(Integer, nullable=False)
    recommendation_summary: Mapped[str] = mapped_column(Text, nullable=False)
    next_action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
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

    opportunity: Mapped[Opportunity] = relationship(
        "Opportunity",
        back_populates="business_plan",
    )
    brand: Mapped[Brand | None] = relationship(
        "Brand",
        back_populates="business_plans",
    )


from app.models.brand import Brand  # noqa: E402,F401
from app.models.opportunity import Opportunity  # noqa: E402,F401
