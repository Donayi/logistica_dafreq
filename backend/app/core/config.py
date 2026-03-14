import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://logistica:logistica123@localhost:5432/logistica_db",
)