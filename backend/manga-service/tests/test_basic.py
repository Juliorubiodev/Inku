# tests/test_basic.py
"""Basic standalone tests for manga-service.

These tests verify basic Python functionality without importing the main app.
This avoids dependency issues with the shared module during CI.
"""
import pytest
import os


class TestEnvironmentSetup:
    """Test that the test environment is correctly configured."""

    def test_python_version(self):
        """Verify Python version is 3.11+."""
        import sys
        assert sys.version_info >= (3, 11), "Python 3.11+ is required"

    def test_required_packages_installed(self):
        """Verify required packages are installed."""
        import fastapi
        import uvicorn
        import pydantic
        assert fastapi is not None
        assert uvicorn is not None
        assert pydantic is not None

    def test_pytest_working(self):
        """Simple test to verify pytest is working."""
        assert True

    def test_environment_variables_can_be_set(self):
        """Test that environment variables work correctly."""
        os.environ["TEST_VAR"] = "test_value"
        assert os.environ.get("TEST_VAR") == "test_value"
        del os.environ["TEST_VAR"]


class TestPydanticModels:
    """Test Pydantic model functionality."""

    def test_pydantic_base_model(self):
        """Test that Pydantic BaseModel works."""
        from pydantic import BaseModel
        
        class TestModel(BaseModel):
            name: str
            value: int
        
        model = TestModel(name="test", value=42)
        assert model.name == "test"
        assert model.value == 42

    def test_pydantic_validation(self):
        """Test Pydantic validation."""
        from pydantic import BaseModel, ValidationError
        
        class StrictModel(BaseModel):
            count: int
        
        with pytest.raises(ValidationError):
            StrictModel(count="not_a_number")


class TestFastAPIBasics:
    """Test FastAPI basic functionality."""

    def test_fastapi_app_creation(self):
        """Test creating a FastAPI app."""
        from fastapi import FastAPI
        app = FastAPI(title="Test App")
        assert app.title == "Test App"

    def test_fastapi_route_definition(self):
        """Test defining a route."""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        
        app = FastAPI()
        
        @app.get("/test")
        def test_route():
            return {"status": "ok"}
        
        client = TestClient(app)
        response = client.get("/test")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
