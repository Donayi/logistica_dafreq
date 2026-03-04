# Login simple para logística (HTML + Tailwind + Node/Postgres)

Instrucciones rápidas para ejecutar localmente:

1. Instalar dependencias

```bash
npm install
```

2. Configurar la base de datos Postgres y variables de entorno

- Crear una base de datos, por ejemplo `logistica_db`.
- Copiar `.env.example` a `.env` y ajustar `DATABASE_URL`.
- Aplicar migración:

```bash
pq -f migrate.sql  # o: psql -d logistica_db -f migrate.sql
```

3. (Opcional) Crear usuario de ejemplo

```bash
npm run create-user
```

4. Iniciar servidor

```bash
npm run dev   # necesita nodemon
# o
npm start
```

5. Abrir `http://localhost:3000` y usar el usuario de ejemplo (ver `.env` o valores por defecto `admin` / `secret123`).

Notas:
- La ruta `POST /api/login` devuelve `{ status: 'ok', profile: {...} }` en caso de éxito.
- Para producción en DigitalOcean configure `DATABASE_URL` con credenciales seguras y use `npm start`.
