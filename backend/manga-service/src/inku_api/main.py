from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .config import settings
from .logging_conf import setup_logging
from .routers import health, mangas, uploads
from .firebase_app import init_firebase

def create_app() -> FastAPI:
    setup_logging(settings.debug)
    app = FastAPI(title="Inku API", version="0.1.0")

    # CORS configuration
    origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def startup():
        init_firebase()
    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(mangas.router,  prefix=settings.api_prefix)
    app.include_router(uploads.router, prefix=settings.api_prefix)
    return app

# 👇 IMPORTANTE: expone 'app' a uvicorn
app = create_app()
