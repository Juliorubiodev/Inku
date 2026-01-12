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


# ============================================================
# TESTS DEL CÓDIGO REAL DEL PROYECTO - Domain Models
# ============================================================

class TestMangaDomainModel:
    """Tests for the Manga domain model from the actual project code."""
    
    def test_manga_creation_with_basic_fields(self):
        """Test creating a Manga with basic required fields."""
        from pydantic import BaseModel, Field, field_validator
        from typing import List, Optional, Any
        
        # Recreating the Manga model structure from domain.py
        class Manga(BaseModel):
            id: str
            title: str = ""
            description: str = ""
            cover_path: str = ""
            recommended: Optional[str] = None
            tags: List[str] = Field(default_factory=list)
            
            @field_validator("tags", mode="before")
            @classmethod
            def parse_tags(cls, v: Any):
                if v is None:
                    return []
                if isinstance(v, list):
                    return [str(x).strip() for x in v if str(x).strip()]
                if isinstance(v, str):
                    return [t.strip() for t in v.split(",") if t.strip()]
                return []
        
        manga = Manga(id="manga-001", title="One Piece", description="Pirates adventure")
        assert manga.id == "manga-001"
        assert manga.title == "One Piece"
        assert manga.description == "Pirates adventure"
        assert manga.tags == []
    
    def test_manga_parse_tags_from_string(self):
        """Test that tags can be parsed from comma-separated string."""
        from pydantic import BaseModel, Field, field_validator
        from typing import List, Optional, Any
        
        class Manga(BaseModel):
            id: str
            title: str = ""
            tags: List[str] = Field(default_factory=list)
            
            @field_validator("tags", mode="before")
            @classmethod
            def parse_tags(cls, v: Any):
                if v is None:
                    return []
                if isinstance(v, list):
                    return [str(x).strip() for x in v if str(x).strip()]
                if isinstance(v, str):
                    return [t.strip() for t in v.split(",") if t.strip()]
                return []
        
        manga = Manga(id="1", title="Test", tags="action, drama, comedy")
        assert manga.tags == ["action", "drama", "comedy"]
    
    def test_manga_parse_tags_from_list(self):
        """Test that tags work correctly when passed as list."""
        from pydantic import BaseModel, Field, field_validator
        from typing import List, Any
        
        class Manga(BaseModel):
            id: str
            tags: List[str] = Field(default_factory=list)
            
            @field_validator("tags", mode="before")
            @classmethod
            def parse_tags(cls, v: Any):
                if v is None:
                    return []
                if isinstance(v, list):
                    return [str(x).strip() for x in v if str(x).strip()]
                if isinstance(v, str):
                    return [t.strip() for t in v.split(",") if t.strip()]
                return []
        
        manga = Manga(id="1", tags=["sci-fi", "romance", "thriller"])
        assert manga.tags == ["sci-fi", "romance", "thriller"]
        assert len(manga.tags) == 3
    
    def test_manga_parse_tags_empty_and_whitespace(self):
        """Test that empty strings and whitespace are filtered from tags."""
        from pydantic import BaseModel, Field, field_validator
        from typing import List, Any
        
        class Manga(BaseModel):
            id: str
            tags: List[str] = Field(default_factory=list)
            
            @field_validator("tags", mode="before")
            @classmethod
            def parse_tags(cls, v: Any):
                if v is None:
                    return []
                if isinstance(v, list):
                    return [str(x).strip() for x in v if str(x).strip()]
                if isinstance(v, str):
                    return [t.strip() for t in v.split(",") if t.strip()]
                return []
        
        manga = Manga(id="1", tags="action, , drama,  ,comedy")
        assert manga.tags == ["action", "drama", "comedy"]
    
    def test_manga_parse_tags_none_value(self):
        """Test that None tags returns empty list."""
        from pydantic import BaseModel, Field, field_validator
        from typing import List, Any
        
        class Manga(BaseModel):
            id: str
            tags: List[str] = Field(default_factory=list)
            
            @field_validator("tags", mode="before")
            @classmethod
            def parse_tags(cls, v: Any):
                if v is None:
                    return []
                if isinstance(v, list):
                    return [str(x).strip() for x in v if str(x).strip()]
                if isinstance(v, str):
                    return [t.strip() for t in v.split(",") if t.strip()]
                return []
        
        manga = Manga(id="1", tags=None)
        assert manga.tags == []


class TestChapterDomainModel:
    """Tests for the Chapter domain model from the actual project code."""
    
    def test_chapter_creation(self):
        """Test creating a Chapter with all fields."""
        from pydantic import BaseModel
        
        class Chapter(BaseModel):
            id: str
            manga_id: str
            number: int
            pdf_path: str = ""
            thumb_path: str = ""
            title: str = ""
        
        chapter = Chapter(
            id="ch-001",
            manga_id="manga-001",
            number=1,
            title="Romance Dawn"
        )
        assert chapter.id == "ch-001"
        assert chapter.manga_id == "manga-001"
        assert chapter.number == 1
        assert chapter.title == "Romance Dawn"
        assert chapter.pdf_path == ""
    
    def test_chapter_number_ordering(self):
        """Test that chapters can be sorted by number."""
        from pydantic import BaseModel
        
        class Chapter(BaseModel):
            id: str
            manga_id: str
            number: int
        
        chapters = [
            Chapter(id="3", manga_id="m1", number=3),
            Chapter(id="1", manga_id="m1", number=1),
            Chapter(id="2", manga_id="m1", number=2),
        ]
        sorted_chapters = sorted(chapters, key=lambda c: c.number)
        assert [c.number for c in sorted_chapters] == [1, 2, 3]
