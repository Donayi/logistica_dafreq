from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.api.v1.router import api_router
from app.routes.evidencias import router as evidencias_router

app = FastAPI(title="Logística - Gestión de Viajes")

# Routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(evidencias_router)  # sin prefix, queda /evidencias/...

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db/ping")
def db_ping(db: Session = Depends(get_db)):
    value = db.execute(text("SELECT 1")).scalar_one()
    return {"db": "ok", "value": value}