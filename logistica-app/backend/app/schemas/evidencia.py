from pydantic import BaseModel

class EvidenciaIn(BaseModel):
    tipo: str
    descripcion: str | None = None
    file_url: str