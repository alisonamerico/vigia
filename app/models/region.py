from geoalchemy2 import Geometry
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Region(Base):
    __tablename__ = 'regions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    geom: Mapped[str] = mapped_column(
        Geometry('POLYGON', srid=4326), nullable=False
    )
    threshold_green: Mapped[float] = mapped_column(Float, default=30.0)
    threshold_yellow: Mapped[float] = mapped_column(Float, default=50.0)
    threshold_orange: Mapped[float] = mapped_column(Float, default=100.0)
    threshold_red: Mapped[float] = mapped_column(Float, default=150.0)
