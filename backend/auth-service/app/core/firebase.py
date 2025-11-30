import firebase_admin
from firebase_admin import credentials, auth
from app.core.config import settings

_firebase_app = None

def init_firebase():
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
    _firebase_app = firebase_admin.initialize_app(cred)
    return _firebase_app

def verify_firebase_token(id_token: str, check_revoked: bool = False) -> dict:
    init_firebase()
    return auth.verify_id_token(id_token, check_revoked=check_revoked)
