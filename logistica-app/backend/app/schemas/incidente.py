from pydantic import BaseModel

class IncidenteIn(BaseModel):
    viaje_id: int
    tipo: str
    lugar: str | None = None
    descripcion: str | None = None