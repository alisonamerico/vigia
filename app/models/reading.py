from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Reading(Base):
    __tablename__ = 'readings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    rain_mm: Mapped[float] = mapped_column(Float, nullable=True)
    river_level_m: Mapped[float] = mapped_column(Float, nullable=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
