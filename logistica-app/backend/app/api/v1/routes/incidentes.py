from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.viaje import Viaje
from app.models.incidente import Incidente
from app.schemas.incidente import IncidenteIn

router = APIRouter()

@router.post("")
def crear_incidente(payload: IncidenteIn, db: Session = Depends(get_db)):
    v = db.get(Viaje, payload.viaje_id)
    if not v:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")

    i = Incidente(**payload.model_dump())
    db.add(i)
    db.commit()
    db.refresh(i)
    return {"id": i.id}