from fastapi import FastAPI
from .config import settings
from .logging_conf import setup_logging
from .routers import health, mangas, uploads
from .firebase_app import init_firebase

def create_app() -> FastAPI:
    setup_logging(settings.debug)
    app = FastAPI(title="Inku API", version="0.1.0")

    @app.on_event("startup")
    def startup():
        init_firebase()
    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(mangas.router,  prefix=settings.api_prefix)
    app.include_router(uploads.router, prefix=settings.api_prefix)
    return app

# 👇 IMPORTANTE: expone 'app' a uvicorn
app = create_app()
     