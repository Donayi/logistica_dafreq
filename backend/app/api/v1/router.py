from fastapi import APIRouter
from app.api.v1.routes import viajes, evidencias, incidentes

api_router = APIRouter()
api_router.include_router(viajes.router, prefix="/viajes", tags=["Viajes"])
api_router.include_router(evidencias.router, prefix="/evidencias", tags=["Evidencias"])
api_router.include_router(incidentes.router, prefix="/incidentes", tags=["Incidentes"])