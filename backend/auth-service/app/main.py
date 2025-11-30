from fastapi import FastAPI
from app.core.config import settings
from app.core.firebase import init_firebase
from app.api.routes import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.SERVICE_NAME, version="0.1.0")

    @app.on_event("startup")
    def _startup():
        init_firebase()

    @app.get("/health")
    def health():
        return {"ok": True, "service": settings.SERVICE_NAME}

    app.include_router(auth_router, prefix=settings.API_PREFIX)
    return app

app = create_app()
