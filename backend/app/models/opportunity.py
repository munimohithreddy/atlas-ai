from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    topic: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    niche: Mapped[str] = mapped_column(String(255), nullable=True)

    demand_score: Mapped[int] = mapped_column(Integer, nullable=False)
    competition_score: Mapped[int] = mapped_column(Integer, nullable=False)
    buyer_intent_score: Mapped[int] = mapped_column(Integer, nullable=False)
    affiliate_score: Mapped[int] = mapped_column(Integer, nullable=False)
    pinterest_score: Mapped[int] = mapped_column(Integer, nullable=False)
    seo_score: Mapped[int] = mapped_column(Integer, nullable=False)

    opportunity_score: Mapped[float] = mapped_column(Float, nullable=False)
    recommendation: Mapped[str] = mapped_column(String(50), nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)

    ai_executive_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_key_strengths: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    ai_key_risks: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    ai_recommendation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_suggested_next_actions: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    business_plan: Mapped[BusinessPlan | None] = relationship(
        "BusinessPlan",
        back_populates="opportunity",
        uselist=False,
    )
    campaigns: Mapped[list["Campaign"]] = relationship("Campaign", back_populates="opportunity")
    evidence: Mapped[list[OpportunityEvidence]] = relationship(
        "OpportunityEvidence",
        back_populates="opportunity",
        cascade="all, delete-orphan",
    )


from app.models.business_plan import BusinessPlan  # noqa: E402,F401
from app.models.campaign import Campaign  # noqa: E402,F401
from app.models.opportunity_evidence import OpportunityEvidence  # noqa: E402,F401
