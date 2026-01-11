"""
Upload router - Presigned URLs and chapter registration with auth.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from shared.auth import get_current_user
from ..services.manga_services import MangaService
from ..adapters.repo_firebase import FirestoreMangaRepo
from ..adapters.s3_aws import Boto3S3Presign
from ..firebase_app import init_firebase
from firebase_admin import firestore as admin_firestore


router = APIRouter(prefix="/uploads", tags=["uploads"])


def get_service() -> MangaService:
    """Dependency to get MangaService with S3."""
    init_firebase()
    db = admin_firestore.client()
    return MangaService(repo=FirestoreMangaRepo(db), s3=Boto3S3Presign())


# Request/Response models

class PresignRequest(BaseModel):
    manga_id: str = Field(..., description="Target manga ID")
    chapter_number: int = Field(..., ge=1, description="Chapter number")
    content_type: str = Field("application/pdf", description="File content type")


class PresignResponse(BaseModel):
    manga_id: str
    chapter_number: int
    s3_key: str
    upload_url: str
    thumb_key: str
    thumb_upload_url: str
    expires_in: int = 900


class RegisterChapterRequest(BaseModel):
    manga_id: str
    chapter_number: int = Field(..., ge=1)
    title: str = Field("", max_length=200)
    s3_key: str
    thumb_key: str = ""


class ChapterResponse(BaseModel):
    id: str
    manga_id: str
    number: int
    title: str
    status: str = "pending_review"


# ============================================
# Authenticated Upload Endpoints
# ============================================

@router.post("/presign", response_model=PresignResponse)
def get_upload_presign(
    request: PresignRequest,
    user: dict = Depends(get_current_user),
    svc: MangaService = Depends(get_service),
):
    """
    Generate presigned URLs for uploading a chapter PDF and thumbnail.
    
    Returns S3 keys and presigned PUT URLs. Frontend uploads directly to S3,
    then calls /register to save metadata.
    """
    try:
        urls = svc.create_upload_urls(
            manga_id=request.manga_id,
            chapter_number=request.chapter_number,
            content_type=request.content_type,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="MANGA_NOT_FOUND")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return PresignResponse(
        manga_id=request.manga_id,
        chapter_number=request.chapter_number,
        s3_key=urls["s3_key"],
        upload_url=urls["upload_url"],
        thumb_key=urls["thumb_key"],
        thumb_upload_url=urls["thumb_upload_url"],
    )


@router.post("/register", response_model=ChapterResponse)
def register_chapter(
    request: RegisterChapterRequest,
    user: dict = Depends(get_current_user),
    svc: MangaService = Depends(get_service),
):
    """
    Register chapter metadata after successful S3 upload.
    
    Sets status to 'pending_review' for moderation.
    """
    try:
        chapter = svc.register_chapter(
            manga_id=request.manga_id,
            chapter_number=request.chapter_number,
            title=request.title,
            s3_key=request.s3_key,
            thumb_key=request.thumb_key,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="MANGA_NOT_FOUND")
    
    return ChapterResponse(
        id=chapter.id,
        manga_id=chapter.manga_id,
        number=chapter.number,
        title=chapter.title,
        status="pending_review",
    )


# ============================================
# Legacy endpoint (for backwards compatibility)
# ============================================

class CreateEpisodeIn(BaseModel):
    episode_id: str
    number: int


@router.post("/mangas/{manga_id}/episodes")
def create_episode_legacy(
    manga_id: str,
    body: CreateEpisodeIn,
    user: dict = Depends(get_current_user),  # Now requires auth
    svc: MangaService = Depends(get_service),
):
    """Legacy endpoint for episode creation."""
    try:
        urls = svc.create_episode_with_presign(
            manga_id=manga_id,
            episode_id=body.episode_id,
            number=body.number,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="MANGA_NOT_FOUND")
    
    return {"manga_id": manga_id, "episode_id": body.episode_id, **urls}
