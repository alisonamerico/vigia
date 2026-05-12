from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Alert(Base):
    __tablename__ = 'alerts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    rain_mm: Mapped[float] = mapped_column(Float, nullable=True)
    river: Mapped[str] = mapped_column(String(100), nullable=True)
    river_level_m: Mapped[float] = mapped_column(Float, nullable=True)
    sources: Mapped[str] = mapped_column(String(500), nullable=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
