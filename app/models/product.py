from sqlalchemy import String, Integer, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100))
    hs_code: Mapped[str] = mapped_column(String(20), index=True)
    origin: Mapped[str] = mapped_column(String(100))
    unit: Mapped[str] = mapped_column(String(20))
    exporter_id: Mapped[int] = mapped_column(Integer, ForeignKey("exporters.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
