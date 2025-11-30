# src/test/conftest.py
import os
import sys
from pathlib import Path
import pytest

# --- Rutas & ENV seguros para Settings ---
THIS = Path(__file__).resolve()
SRC_DIR = THIS.parents[1]
sys.path.insert(0, str(SRC_DIR))

os.environ.setdefault("API_PREFIX", "/api")
os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("FIREBASE_PROJECT_ID", "inku-app-test")
os.environ.setdefault("FIREBASE_CRED_FILE", str(SRC_DIR / "test" / "dummy-firebase.json"))
os.environ.setdefault("AWS_REGION", "eu-north-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test")
os.environ.setdefault("S3_BUCKET_NAME", "test-bucket")
os.environ.setdefault("S3_PRESIGN_EXPIRES_SECONDS", "900")

from inku_api.domain import Manga  # noqa: E402
from inku_api.services.manga_services import MangaService  # noqa: E402
from inku_api.adapters import repo_firebase as rf  # noqa: E402
from inku_api.adapters import s3_presign as s3ps   # noqa: E402
from inku_api.routers import mangas, uploads       # noqa: E402


# -------- Dobles de prueba --------
class InMemoryRepo:
    def __init__(self):
        # guardamos un Manga por si alguna otra ruta lo pidiera,
        # pero la ruta /api/mangas SOLO espera devolver IDs (str)
        self._m1 = Manga(id="m1", title="One Test", description="desc")

    # 👇 ESTE es el fix: devolver lista de STR (IDs), no objetos
    def list_mangas(self):
        return ["m1"]

    def get_manga(self, manga_id: str):
        return self._m1 if manga_id == "m1" else None

    def list_episodes(self, manga_id: str):
        return []

    def get_episode_by_id(self, manga_id: str, episode_id: str):
        return None

    def get_episode_by_number(self, manga_id: str, number: int):
        return None


class FakeS3:
    def presign_put(self, key: str, content_type: str, expires: int = 900) -> str:
        return f"https://example.com/put/{key}"

    def presign_get(self, key: str, expires: int = 900) -> str:
        return f"https://example.com/get/{key}"


@pytest.fixture
def app_client(monkeypatch):
    # Evitar tocar Firebase/S3 reales
    monkeypatch.setattr(rf, "FirestoreMangaRepo", InMemoryRepo, raising=True)
    monkeypatch.setattr(s3ps, "Boto3S3Presign", FakeS3, raising=True)

    # Blindaje si firebase_admin se inicializa en algún sitio
    try:
        import firebase_admin  # noqa: F401
        monkeypatch.setattr("firebase_admin.initialize_app", lambda *a, **k: object(), raising=False)
        monkeypatch.setattr("firebase_admin.get_app", lambda *a, **k: object(), raising=False)
        monkeypatch.setattr("firebase_admin.credentials.Certificate", lambda *a, **k: object(), raising=False)
        monkeypatch.setattr("firebase_admin.firestore.client", lambda *a, **k: object(), raising=False)
    except Exception:
        pass

    from fastapi.testclient import TestClient
    from inku_api.main import create_app

    app = create_app()

    def _fake_service():
        return MangaService(repo=InMemoryRepo(), s3=FakeS3())

    # Overrides explícitos por si el router usa Depends(get_service)
    app.dependency_overrides[getattr(mangas, "get_service")] = _fake_service
    app.dependency_overrides[getattr(uploads, "get_service")] = _fake_service

    return TestClient(app)
