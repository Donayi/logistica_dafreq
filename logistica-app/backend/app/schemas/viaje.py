from datetime import date
from pydantic import BaseModel

class ViajeInicioIn(BaseModel):
    id_viaje: str
    cliente: str
    origen: str
    destino: str
    trailer: str
    caja: str
    tipo_carga: str | None = None
    peso_caja: float | None = None
    fecha_entrega_programada: date | None = None
    combustible_salida: float | None = None
    kilometraje_salida: int | None = None

class ViajeCierreIn(BaseModel):
    fecha_entregada: date | None = None
    sellos_recibido: str | None = None
    claves_maniobra_dhl: str | None = None