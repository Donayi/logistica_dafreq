from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Evidencia(Base):
    __tablename__ = "evidencias"

    id: Mapped[int] = mapped_column(primary_key=True)

    viaje_id: Mapped[int] = mapped_column(ForeignKey("viajes.id"), nullable=False)

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)  # documento|sello|foto|otro
    descripcion: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # En MVP guardamos URL/Key (luego R2)
    file_url: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    viaje = relationship("Viaje", back_populates="evidencias")