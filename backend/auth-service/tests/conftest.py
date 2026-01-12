# tests/conftest.py
"""Test fixtures for auth-service."""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add app to path
THIS = Path(__file__).resolve()
APP_DIR = THIS.parents[1]
sys.path.insert(0, str(APP_DIR))

# Set required environment variables
os.environ.setdefault("FIREBASE_SERVICE_ACCOUNT_PATH", "/fake/path.json")
os.environ.setdefault("FIREBASE_WEB_API_KEY", "fake-api-key")
os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")
os.environ.setdefault("API_PREFIX", "/api")
os.environ.setdefault("SERVICE_NAME", "auth-service")


@pytest.fixture(scope="session", autouse=True)
def mock_firebase():
    """Mock Firebase Admin SDK to avoid initialization errors."""
    # Mock firebase_admin module
    mock_firebase_admin = MagicMock()
    mock_firebase_admin.initialize_app = MagicMock(return_value=MagicMock())
    mock_firebase_admin.get_app = MagicMock(return_value=MagicMock())
    mock_firebase_admin.App = MagicMock()
    
    # Mock credentials
    mock_credentials = MagicMock()
    mock_credentials.Certificate = MagicMock(return_value=MagicMock())
    mock_firebase_admin.credentials = mock_credentials
    
    # Mock auth
    mock_auth = MagicMock()
    mock_auth.verify_id_token = MagicMock(return_value={
        "uid": "test-user-123",
        "email": "test@example.com",
        "name": "Test User",
    })
    mock_firebase_admin.auth = mock_auth
    
    # Patch the modules
    sys.modules["firebase_admin"] = mock_firebase_admin
    sys.modules["firebase_admin.credentials"] = mock_credentials
    sys.modules["firebase_admin.auth"] = mock_auth
    
    # Mock shared.auth
    mock_shared = MagicMock()
    mock_shared.auth = MagicMock()
    mock_shared.auth.init_firebase = MagicMock(return_value=MagicMock())
    mock_shared.auth.verify_firebase_token = MagicMock(return_value={
        "uid": "test-user-123",
        "email": "test@example.com",
    })
    sys.modules["shared"] = mock_shared
    sys.modules["shared.auth"] = mock_shared.auth
    
    yield mock_firebase_admin


@pytest.fixture
def app_client(mock_firebase):
    """Create a test client for the FastAPI app."""
    from fastapi.testclient import TestClient
    
    # Patch init_firebase before importing app
    with patch("app.core.firebase.init_firebase", return_value=None):
        from app.main import create_app
        app = create_app()
        
        # Override startup to not call init_firebase
        app.router.on_startup = []
        
        return TestClient(app)
