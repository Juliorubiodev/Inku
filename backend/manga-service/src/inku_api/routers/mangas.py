"""
Manga router - Catalog, detail, and chapters endpoints.
"""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from firebase_admin import firestore as admin_firestore

from ..firebase_app import init_firebase
from ..services.manga_services import MangaService
from ..adapters.repo_firebase import FirestoreMangaRepo
from ..adapters.s3_aws import Boto3S3Presign
from ..domain import Manga, Chapter
from shared.auth import get_current_user

router = APIRouter(prefix="/mangas", tags=["mangas"])


def get_service() -> MangaService:
    """Dependency to get MangaService with repo and S3."""
    init_firebase()
    db = admin_firestore.client()
    repo = FirestoreMangaRepo(db)
    s3 = Boto3S3Presign()
    return MangaService(repo=repo, s3=s3)


# Response models
class MangaWithCover(BaseModel):
    id: str
    title: str
    description: str
    cover_path: Optional[str] = None  # Original path from Firestore
    cover_url: Optional[str] = None   # Resolved URL (presigned or direct)
    recommended: Optional[str] = None
    tags: List[str] = []


class ChapterWithUrl(BaseModel):
    id: str
    manga_id: str
    number: int
    title: str
    read_url: Optional[str] = None


class CreateMangaRequest(BaseModel):
    """Request body for creating a new manga."""
    id: str  # slug/id for the manga
    title: str
    description: str = ""
    recommended: Optional[str] = None
    tags: List[str] = []
    cover_path: Optional[str] = None


# ============================================
# Authenticated Endpoints
# ============================================

@router.post("", response_model=MangaWithCover, status_code=201)
def create_manga(
    request: CreateMangaRequest,
    user: dict = Depends(get_current_user),
    svc: MangaService = Depends(get_service),
):
    """Create a new manga entry. Requires authentication. Used when uploading a new manga with its first chapter."""
    from ..domain import Manga
    
    # Check if manga already exists
    if svc.repo.manga_exists(request.id):
        raise HTTPException(status_code=409, detail="MANGA_ALREADY_EXISTS")
    
    manga = Manga(
        id=request.id,
        title=request.title,
        description=request.description,
        cover_path=request.cover_path or "",
        recommended=request.recommended,
        tags=request.tags,
    )
    
    try:
        created = svc.create_manga(manga)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    return MangaWithCover(
        id=created.id,
        title=created.title,
        description=created.description,
        cover_path=created.cover_path,
        cover_url=None,  # No cover uploaded yet
        recommended=created.recommended,
        tags=created.tags,
    )


# ============================================
# Public Endpoints
# ============================================

@router.get("", response_model=List[MangaWithCover])
def list_mangas(svc: MangaService = Depends(get_service)) -> List[MangaWithCover]:
    """Get all mangas from catalog with cover URLs."""
    mangas = svc.list_mangas()
    result = []
    for manga in mangas:
        cover_url = None
        if manga.cover_path:
            try:
                cover_url = svc.get_cover_url(manga)
            except Exception:
                pass
        result.append(MangaWithCover(
            id=manga.id,
            title=manga.title,
            description=manga.description,
            cover_path=manga.cover_path,
            cover_url=cover_url,
            recommended=manga.recommended,
            tags=manga.tags,
        ))
    return result


@router.get("/{manga_id}", response_model=MangaWithCover)
def get_manga(
    manga_id: str,
    include_cover: bool = Query(True, description="Include presigned cover URL"),
    svc: MangaService = Depends(get_service),
):
    """Get manga details by ID with optional presigned cover URL."""
    manga = svc.get_manga(manga_id)
    if manga is None:
        raise HTTPException(status_code=404, detail="MANGA_NOT_FOUND")
    
    cover_url = None
    if include_cover and manga.cover_path:
        try:
            cover_url = svc.get_cover_url(manga)
        except Exception:
            pass  # S3 might not be configured
    
    return MangaWithCover(
        id=manga.id,
        title=manga.title,
        description=manga.description,
        cover_path=manga.cover_path,
        cover_url=cover_url,
        recommended=manga.recommended,
        tags=manga.tags,
    )


@router.get("/{manga_id}/chapters", response_model=List[Chapter])
def list_chapters(
    manga_id: str,
    sort: str = Query("asc", regex="^(asc|desc)$", description="Sort order by chapter number"),
    svc: MangaService = Depends(get_service),
) -> List[Chapter]:
    """Get all chapters for a manga, ordered by number."""
    try:
        chapters = svc.list_chapters(manga_id)
        # Sort by chapter number
        reverse = (sort == "desc")
        return sorted(chapters, key=lambda c: c.number, reverse=reverse)
    except KeyError:
        raise HTTPException(status_code=404, detail="MANGA_NOT_FOUND")


@router.get("/{manga_id}/chapters/{chapter_id}", response_model=ChapterWithUrl)
def get_chapter(
    manga_id: str,
    chapter_id: str,
    include_url: bool = Query(True, description="Include presigned read URL"),
    svc: MangaService = Depends(get_service),
):
    """Get chapter details with optional presigned read URL for PDF."""
    chapter = svc.get_chapter(manga_id, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="CHAPTER_NOT_FOUND")
    
    read_url = None
    if include_url and chapter.pdf_path:
        try:
            read_url = svc.get_read_url(chapter)
        except Exception:
            pass
    
    return ChapterWithUrl(
        id=chapter.id,
        manga_id=chapter.manga_id,
        number=chapter.number,
        title=chapter.title,
        read_url=read_url,
    )


@router.get("/{manga_id}/chapters/{chapter_id}/read-url")
def get_read_url(
    manga_id: str,
    chapter_id: str,
    expires: int = Query(900, ge=60, le=3600, description="URL expiration in seconds"),
    svc: MangaService = Depends(get_service),
):
    """Get presigned URL for reading chapter PDF."""
    chapter = svc.get_chapter(manga_id, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="CHAPTER_NOT_FOUND")
    
    if not chapter.pdf_path:
        raise HTTPException(status_code=404, detail="CHAPTER_HAS_NO_PDF")
    
    try:
        url = svc.get_read_url(chapter, expires=expires)
        return {
            "url": url,
            "expires_in": expires,
            "content_type": "application/pdf",
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
