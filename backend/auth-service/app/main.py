from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.core.config import settings
from app.core.firebase import init_firebase
from app.api.routes import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.SERVICE_NAME, version="0.1.0")

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
    def _startup():
        init_firebase()

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok", "service": settings.SERVICE_NAME}

    app.include_router(auth_router, prefix=settings.API_PREFIX)
    return app

app = create_app()
