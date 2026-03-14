from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Incidente(Base):
    __tablename__ = "incidentes"

    id: Mapped[int] = mapped_column(primary_key=True)
    viaje_id: Mapped[int] = mapped_column(ForeignKey("viajes.id"), nullable=False)

    tipo: Mapped[str] = mapped_column(String(30), nullable=False)  # falla|siniestro|otro
    lugar: Mapped[str] = mapped_column(String(200), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    viaje = relationship("Viaje", back_populates="incidentes")