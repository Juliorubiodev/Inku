import firebase_admin
from firebase_admin import credentials
from .config import settings

_initialized = False

def init_firebase() -> None:
    global _initialized
    if _initialized:
        return
    if firebase_admin._apps:
        _initialized = True
        return

    cred = credentials.Certificate(settings.firebase_cred_file)
    firebase_admin.initialize_app(cred, {"projectId": settings.firebase_project_id})
    _initialized = True
