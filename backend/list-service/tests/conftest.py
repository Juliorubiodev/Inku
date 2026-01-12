# tests/conftest.py
"""Test fixtures for list-service."""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path
THIS = Path(__file__).resolve()
SRC_DIR = THIS.parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

# Mock shared.auth before importing the app
@pytest.fixture(scope="session", autouse=True)
def mock_shared_auth():
    """Mock Firebase dependencies to avoid initialization."""
    mock_user = {"uid": "test-user-123", "email": "test@example.com", "name": "Test User"}
    
    with patch.dict(os.environ, {
        "FIREBASE_SERVICE_ACCOUNT_PATH": "/fake/path.json",
        "CORS_ORIGINS": "http://localhost:3000",
    }):
        # Mock the shared.auth module
        mock_auth = MagicMock()
        mock_auth.init_firebase = MagicMock(return_value=MagicMock())
        mock_auth.get_current_user = MagicMock(return_value=mock_user)
        mock_auth.get_optional_user = MagicMock(return_value=mock_user)
        
        sys.modules["shared"] = MagicMock()
        sys.modules["shared.auth"] = mock_auth
        
        yield mock_auth


@pytest.fixture
def app_client(mock_shared_auth):
    """Create a test client for the FastAPI app."""
    from fastapi.testclient import TestClient
    
    # Import app after mocking
    from list_service.main import app
    
    # Override dependencies
    mock_user = {"uid": "test-user-123", "email": "test@example.com", "name": "Test User"}
    
    def fake_get_current_user():
        return mock_user
    
    def fake_get_optional_user():
        return mock_user
    
    # Import the actual dependency functions to override them
    from shared.auth import get_current_user, get_optional_user
    app.dependency_overrides[get_current_user] = fake_get_current_user
    app.dependency_overrides[get_optional_user] = fake_get_optional_user
    
    # Mock the repository
    from list_service.repository import FirestoreListRepo
    from list_service.main import get_repo
    
    mock_repo = MagicMock(spec=FirestoreListRepo)
    mock_repo.get_public.return_value = ([], 0)
    mock_repo.get_by_owner.return_value = []
    
    app.dependency_overrides[get_repo] = lambda: mock_repo
    
    return TestClient(app)
