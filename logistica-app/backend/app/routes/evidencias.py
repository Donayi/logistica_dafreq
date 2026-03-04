from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.r2_service import build_file_key, presign_put, presign_get, head_object

router = APIRouter(prefix="/evidencias", tags=["Evidencias"])

class PresignUploadRequest(BaseModel):
    viaje_id: int
    category: str = Field(pattern="^(inicio|fin|averia|docs)$")
    filename: str
    content_type: str

@router.post("/presign-upload")
def presign_upload(data: PresignUploadRequest):
    if not data.content_type:
        raise HTTPException(status_code=400, detail="content_type requerido")
    file_key = build_file_key(data.viaje_id, data.category, data.filename)
    upload_url = presign_put(file_key, data.content_type, expires_seconds=600)
    return {"upload_url": upload_url, "file_key": file_key}

class PresignDownloadRequest(BaseModel):
    file_key: str
    download_filename: str | None = None

@router.post("/presign-download")
def presign_download(data: PresignDownloadRequest):
    download_url = presign_get(
        file_key=data.file_key,
        download_filename=data.download_filename,
        expires_seconds=120,
    )
    return {"download_url": download_url}

class RegisterEvidenceRequest(BaseModel):
    viaje_id: int
    category: str = Field(pattern="^(inicio|fin|averia|docs)$")
    file_key: str
    original_filename: str

@router.post("")
def register_evidence(data: RegisterEvidenceRequest):
    # Aquí después conectamos a BD (Postgres) para guardar la evidencia.
    # Por ahora validamos que el objeto realmente exista en R2:
    try:
        meta = head_object(data.file_key)
    except Exception:
        raise HTTPException(status_code=400, detail="El archivo no existe en R2 (aún no se subió o key incorrecta)")

    return {
        "viaje_id": data.viaje_id,
        "category": data.category,
        "file_key": data.file_key,
        "original_filename": data.original_filename,
        "size_bytes": meta.get("ContentLength"),
        "content_type": meta.get("ContentType"),
    }