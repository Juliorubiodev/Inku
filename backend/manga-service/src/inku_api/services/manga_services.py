from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Union, Dict, Any
from urllib.parse import urlparse, unquote
from ..domain import Chapter, Manga
from ..ports import MangaRepository, S3PresignService


@dataclass
class MangaService:
    """Service layer for manga operations."""
    repo: MangaRepository
    s3: Optional[S3PresignService] = None
    
    # ---- Mangas ----
    
    def list_mangas(self) -> List[Manga]:
        """Get all mangas from catalog."""
        return list(self.repo.list_mangas())
    
    def get_manga(self, manga_id: str) -> Optional[Manga]:
        """Get manga details by ID."""
        return self.repo.get_manga(manga_id)
    
    def create_manga(self, manga: Manga) -> Manga:
        """Create a new manga entry."""
        return self.repo.create_manga(manga)
    
    # ---- Chapters ----

    def list_chapters(self, manga_id: str) -> List[Chapter]:
        """Get all chapters for a manga."""
        if not self.repo.manga_exists(manga_id):
            raise KeyError("MANGA_NOT_FOUND")
        return list(self.repo.list_chapters(manga_id))

    def get_chapter(self, manga_id: str, ident: Union[str, int]) -> Optional[Chapter]:
        """Get chapter by ID or number."""
        if isinstance(ident, int) or (isinstance(ident, str) and ident.isdigit()):
            return self.repo.get_chapter_by_number(manga_id, int(ident))
        else:
            return self.repo.get_chapter_by_id(manga_id, ident)
    
    # ---- Reading (presigned GET URLs) ----

    def get_read_url(self, chapter: Chapter, expires: int = 900) -> str:
        """Generate presigned URL for reading chapter PDF."""
        if self.s3 is None:
            raise ValueError("S3 service not configured")
        if not chapter.pdf_path:
            raise ValueError("Chapter has no PDF path")
        
        path = chapter.pdf_path
        
        # Helper to extract key from S3 URL
        if path.startswith("http://") or path.startswith("https://"):
            # Check if it looks like an S3 URL (amazonaws.com)
            if "amazonaws.com" in path:
                try:
                    parsed = urlparse(path)
                    # path from url includes leading slash, e.g. /chapters/foo.pdf
                    # We need chapters/foo.pdf
                    processed_path = parsed.path.lstrip('/')
                    # Decode URL encoding (e.g. Sakamoto+Days -> Sakamoto Days)
                    path = unquote(processed_path)
                except Exception:
                    # If parsing fails, fall back to returning original (might fail reading)
                    return path
            else:
                # External non-S3 URL, return as is (assumed public)
                return path

        return self.s3.presign_get(path, expires=expires)
    
    def get_cover_url(self, manga: Manga, expires: int = 900) -> Optional[str]:
        """Generate presigned URL for manga cover image.
        
        If cover_path is already a complete URL (starts with http), return it directly.
        Otherwise, treat it as an S3 key and generate a presigned URL.
        """
        if not manga.cover_path:
            return None
        
        # If cover_path is already a full URL, return it directly
        if manga.cover_path.startswith("http://") or manga.cover_path.startswith("https://"):
            return manga.cover_path
        
        # Otherwise, generate presigned URL from S3 key
        if self.s3 is None:
            return None
        return self.s3.presign_get(manga.cover_path, expires=expires)
    
    # ---- Uploads (presigned PUT URLs) ----

    def create_upload_urls(
        self, 
        manga_id: str, 
        chapter_number: int,
        content_type: str = "application/pdf",
    ) -> Dict[str, Any]:
        """
        Generate presigned URLs for uploading a new chapter.
        Returns S3 key and upload URL.
        """
        if self.s3 is None:
            raise ValueError("S3 service not configured")
        if not self.repo.manga_exists(manga_id):
            raise KeyError("MANGA_NOT_FOUND")
        
        # Generate S3 key for the chapter
        s3_key = f"chapters/{manga_id}/{chapter_number}.pdf"
        thumb_key = f"thumbnails/{manga_id}/{chapter_number}.jpg"
        
        return {
            "s3_key": s3_key,
            "upload_url": self.s3.presign_put(s3_key, content_type=content_type),
            "thumb_key": thumb_key,
            "thumb_upload_url": self.s3.presign_put(thumb_key, content_type="image/jpeg"),
        }
    
    def register_chapter(
        self,
        manga_id: str,
        chapter_number: int,
        title: str,
        s3_key: str,
        thumb_key: str = "",
        status: str = "pending_review",
    ) -> Chapter:
        """
        Register chapter metadata after upload.
        Status can be: pending_review, approved, rejected
        """
        if not self.repo.manga_exists(manga_id):
            raise KeyError("MANGA_NOT_FOUND")
        
        chapter = Chapter(
            id=f"{manga_id}-ch{chapter_number}",
            manga_id=manga_id,
            number=chapter_number,
            title=title,
            pdf_path=s3_key,
            thumb_path=thumb_key,
        )
        
        return self.repo.create_chapter(chapter)

    # Legacy method for compatibility
    def create_episode_with_presign(
        self, 
        manga_id: str, 
        episode_id: str, 
        number: int
    ) -> Dict[str, Any]:
        """Legacy method - creates upload URLs for an episode."""
        urls = self.create_upload_urls(manga_id, number)
        return {
            "upload_url": urls["upload_url"],
            "s3_key": urls["s3_key"],
        }
