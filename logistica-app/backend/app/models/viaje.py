from datetime import datetime, date
from sqlalchemy import String, DateTime, Date, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Viaje(Base):
    __tablename__ = "viajes"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Identidad / negocio
    id_viaje: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    cliente: Mapped[str] = mapped_column(String(200), nullable=False)

    origen: Mapped[str] = mapped_column(String(200), nullable=False)
    destino: Mapped[str] = mapped_column(String(200), nullable=False)

    trailer: Mapped[str] = mapped_column(String(80), nullable=False)
    caja: Mapped[str] = mapped_column(String(80), nullable=False)

    tipo_carga: Mapped[str] = mapped_column(String(120), nullable=True)
    peso_caja: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Fechas
    fecha_salida: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_entrega_programada: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Inicio
    combustible_salida: Mapped[float | None] = mapped_column(Float, nullable=True)
    kilometraje_salida: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Cierre
    fecha_entregada: Mapped[date | None] = mapped_column(Date, nullable=True)
    sellos_recibido: Mapped[str | None] = mapped_column(String(200), nullable=True)
    claves_maniobra_dhl: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Estado
    status: Mapped[str] = mapped_column(String(30), default="ABIERTO", nullable=False)  # ABIERTO|CERRADO

    # Relaciones
    evidencias = relationship("Evidencia", back_populates="viaje")
    incidentes = relationship("Incidente", back_populates="viaje")