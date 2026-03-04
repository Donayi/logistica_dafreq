import os
from uuid import uuid4
from datetime import datetime

import boto3
from botocore.client import Config

R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_ACCESS_KEY = os.getenv('R2_ACCESS_KEY')
R2_SECRET_KEY = os.getenv('R2_SECRET_KEY')
R2_BUCKET = os.getenv('R2_BUCKET')


def s3_client():
    if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET]):
        raise RuntimeError('Faltan variables R2_* en el contenedor')
    return boto3.client(
        's3',
        endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto',
    )


def build_file_key(viaje_id: int, category: str, original_filename: str) -> str:
    # NO metemos el nombre real del archivo en el key (privacidad).
    # Tomamos solo la extensión para mantener compatibilidad.
    _, ext = os.path.splitext(original_filename or '')
    ext = (ext or '').lower().strip('.')
    if not ext:
        ext = 'bin'

    now = datetime.utcnow()
    return f'viajes/{viaje_id}/{category}/{now.year}/{now.month:02d}/{uuid4()}.{ext}'


def presign_put(file_key: str, content_type: str, expires_seconds: int = 1800) -> str:
    # 30 minutos en dev para evitar expiraciones mientras pruebas
    s3 = s3_client()
    return s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': R2_BUCKET,
            'Key': file_key,
            'ContentType': content_type,
        },
        ExpiresIn=expires_seconds,
    )


def presign_get(file_key: str, download_filename: str | None = None, expires_seconds: int = 300) -> str:
    # 5 minutos en dev
    s3 = s3_client()
    params = {'Bucket': R2_BUCKET, 'Key': file_key}
    if download_filename:
        params['ResponseContentDisposition'] = f'attachment; filename=\"{download_filename}\"'
    return s3.generate_presigned_url(
        ClientMethod='get_object',
        Params=params,
        ExpiresIn=expires_seconds,
    )


def head_object(file_key: str):
    s3 = s3_client()
    return s3.head_object(Bucket=R2_BUCKET, Key=file_key)