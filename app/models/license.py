from datetime import datetime, timezone
from sqlalchemy import String, Integer, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class License(Base):
    __tablename__ = "licenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    exporter_id: Mapped[int] = mapped_column(Integer, ForeignKey("exporters.id"), nullable=False)
    market_id: Mapped[int] = mapped_column(Integer, ForeignKey("markets.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    notes: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
