from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OpportunityEvidence(Base):
    __tablename__ = "opportunity_evidence"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id"),
        nullable=False,
        index=True,
    )
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    opportunity: Mapped["Opportunity"] = relationship(back_populates="evidence")
