from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AffiliateProgram(Base):
    __tablename__ = "affiliate_programs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    network: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    website_url: Mapped[str] = mapped_column(String(500), nullable=False)
    commission_type: Mapped[str] = mapped_column(String(100), nullable=False)
    commission_rate: Mapped[float] = mapped_column(Float, nullable=False)
    cookie_duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
