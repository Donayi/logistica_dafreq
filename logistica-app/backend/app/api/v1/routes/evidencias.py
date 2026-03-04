from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.viaje import Viaje
from app.models.evidencia import Evidencia
from app.schemas.evidencia import EvidenciaIn

router = APIRouter()

@router.post("/viaje/{viaje_id}")
def agregar_evidencia(viaje_id: int, payload: EvidenciaIn, db: Session = Depends(get_db)):
    v = db.get(Viaje, viaje_id)
    if not v:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")

    e = Evidencia(viaje_id=viaje_id, **payload.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    return {"id": e.id}