from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Finance(Base):
    __tablename__ = "finance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    license_id: Mapped[int] = mapped_column(Integer, ForeignKey("licenses.id"), nullable=False)
    exporter_id: Mapped[int] = mapped_column(Integer, ForeignKey("exporters.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    fee_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
