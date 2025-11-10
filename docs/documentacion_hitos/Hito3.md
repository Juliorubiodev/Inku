# Hito 3 – Arquitectura por capas, DI, logs y tests (Backend Inku)

**Proyecto: Inku** — microservicio backend para lectura de manga
                    
**Stack:** FastAPI · Pydantic · Firestore (prod) · AWS S3 presign (prod) · Pytest · GitHub Actions
                
**Estado:** ✅ Tests verdes (2/2), logs activos, DI aplicada, documentación incluida

### 🎯 Objetivo del hito

Diseñar, documentar y testear el microservicio backend de Inku con una arquitectura desacoplada por capas, inyección de dependencias (DI), registro de actividad (logs) y tests reproducibles.
El servicio debe poder ejecutarse en local con dependencias simuladas y en producción con Firebase Firestore (datos) y AWS S3 (presign de PDFs).

### 🧰 Tecnologías y dependencias utilizadas
| Tipo                  | Herramienta / Librería                 | Versión (aprox.) | Propósito                         |
| --------------------- | -------------------------------------- | ---------------- | --------------------------------- |
| Framework web         | FastAPI                                | 0.11x            | API REST (ASGI/Starlette)         |
| Servidor ASGI         | Uvicorn                                | 0.30.x           | Servidor de desarrollo            |
| Validación / Modelado | Pydantic v2                            | 2.9.x            | Modelos/DTOs y validación         |
| Config por entorno    | pydantic-settings                      | 2.x              | Variables de entorno y `.env`     |
| Firestore (prod)      | firebase-admin, google-cloud-firestore | —                | Acceso a BD (producción)          |
| AWS S3 (prod)         | boto3                                  | —                | URLs firmadas (lectura/escritura) |
| Cliente HTTP test     | httpx (via TestClient)                 | —                | Test funcionales                  |
| Tests                 | pytest                                 | —                | Framework de pruebas              |
| Logs                  | logging (stdlib)                       | —                | Registro de actividad             |
| CI/CD                 | GitHub Actions                         | —                | Tests automáticos por push/PR     |




### Justificación de FastAPI

Alto rendimiento (ASGI), OpenAPI y documentación automática.

Tipado fuerte + Pydantic v2 → validación segura entre capas.

Dependencias y DI integradas → sustituimos Firestore/S3 por dobles en tests sin tocar el código.

Excelente testabilidad con TestClient.

### 🧩 Diseño de la API, rutas y arquitectura por capas
Estructura del proyecto

backend/

    └── src/
    └── inku_api/
        ├── main.py                  # create_app(), montaje de routers y logging
        ├── config.py                # Settings pydantic-settings (aliases y .env)
        ├── logging_conf.py          # Config de logging
        ├── domain.py                # Modelos de dominio (Manga, Episode)
        ├── services/
        │   └── manga_services.py    # Lógica de negocio (MangaService)
        ├── adapters/
        │   ├── repo_firebase.py     # FirestoreMangaRepo (producción)
        │   └── s3_presign.py        # Boto3S3Presign (producción)
        └── routers/
            ├── health.py            # /health
            └── mangas.py            # /mangas y subrutas
    └── test/
        ├── conftest.py              # TestClient y monkeypatch de dependencias
        ├── test_health.py           # Test /api/health
        └── test_mangas_api.py       # Test /api/mangas (listado)



Ventaja: la API queda delgada, la lógica testeable y los puntos de acceso a infra contenidos.

### 🔌 Endpoints expuestos

Prefijo global: ${API_PREFIX} (por defecto /api)

GET /api/health → {"status": "ok"}

GET /api/mangas → Lista de mangas

(Definidos pero no exigidos en este hito)

GET /api/mangas/{manga_id}

GET /api/mangas/{manga_id}/episodes


Ejemplos rápidos

 HTTPie

http :8000/api/health

http :8000/api/mangas

http: 8000/api/mangas/sakamoto-days/episodes

 PowerShell

Invoke-RestMethod -Method GET http://127.0.0.1:8000/api/health

Invoke-RestMethod -Method GET http://127.0.0.1:8000/api/mangas

Invoke-RestMethod -Method GET http://127.0.0.1:8000/api/mangas/sakamoto-days/episodes




### 🗒️ Logs

Config global en logging_conf.py e inicialización en create_app().

Mensajes informativos en arranque y al inicializar presigner S3 (bucket/region).

Captura y log de errores de capa adaptador/servicio.

Ejemplo de middleware de request

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        logger.info("Status: %s", response.status_code)
        return response
    except Exception:
        logger.exception("Unhandled error")
        raise

### 🧪 Tests (unitarios/funcionales) y DI

Estrategia

Los routers usan un get_service()

**Probado:**

**Revisar la captura de pantalla**

### Ejecución local

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt


pytest -q


***Resultado actual: 2 passed ✅***

▶️ Ejecución del servidor (local)

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt


# Arrancar
python -m uvicorn inku_api.main:app --app-dir src --reload --reload-dir src

# Probar
### http://127.0.0.1:8000/api/health
### http://127.0.0.1:8000/api/mangas
### http://127.0.0.1:8000/api/mangas/sakamoto-days/episodes



## 🤖 CI – GitHub Actions

Workflow: .github/workflows/backend-ci.yml

Python 3.11.

Instala dependencias, lint mínimo y pytest -q.

Working directory: backend/.

name: Backend CI


# 🔚 Conclusión

El microservicio Inku cumple los objetivos del hito: API REST limpia y desacoplada, servicios con DI, adaptadores a Firestore y S3 aislados, logs consistentes y tests verdes sin tocar infra real.
La base está lista para ampliar endpoints (episodes, read, auth) y endurecer validaciones en hitos posteriores.
