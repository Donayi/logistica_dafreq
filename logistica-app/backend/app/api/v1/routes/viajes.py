from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.viaje import Viaje
from app.schemas.viaje import ViajeInicioIn, ViajeCierreIn

router = APIRouter()

@router.post("/inicio")
def iniciar_viaje(payload: ViajeInicioIn, db: Session = Depends(get_db)):
    v = Viaje(**payload.model_dump())
    db.add(v)
    db.commit()
    db.refresh(v)
    return {"id": v.id, "status": v.status}

@router.post("/{viaje_id}/cierre")
def cerrar_viaje(viaje_id: int, payload: ViajeCierreIn, db: Session = Depends(get_db)):
    v = db.get(Viaje, viaje_id)
    if not v:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    if v.status == "CERRADO":
        raise HTTPException(status_code=409, detail="Viaje ya cerrado")

    for k, val in payload.model_dump().items():
        setattr(v, k, val)

    v.status = "CERRADO"
    db.commit()
    return {"id": v.id, "status": v.status}