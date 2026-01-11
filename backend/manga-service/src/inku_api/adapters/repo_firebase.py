from __future__ import annotations
import logging
from typing import Iterable, Optional

from firebase_admin import firestore as admin_firestore

from ..domain import Chapter, Manga
from ..ports import MangaRepository

logger = logging.getLogger(__name__)

class FirestoreMangaRepo(MangaRepository):
    def __init__(self, db: admin_firestore.Client):
        self._db = db

    def list_mangas(self) -> Iterable[Manga]:
        snaps = self._db.collection("mangas").stream()
        for doc in snaps:
            data = doc.to_dict() or {}
            yield Manga(
                id=doc.id,
                title=data.get("title", "") or "",
                description=data.get("description", "") or "",
                cover_path=data.get("cover_path", "") or "",
                recommended=data.get("recommended"),
                tags=data.get("tags"),
            )

    def manga_exists(self, manga_id: str) -> bool:
        return self._db.collection("mangas").document(manga_id).get().exists

    def get_manga(self, manga_id: str) -> Optional[Manga]:
        """Get a single manga by ID."""
        doc = self._db.collection("mangas").document(manga_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict() or {}
        return Manga(
            id=doc.id,
            title=data.get("title", "") or "",
            description=data.get("description", "") or "",
            cover_path=data.get("cover_path", "") or "",
            recommended=data.get("recommended"),
            tags=data.get("tags"),
        )

    def create_manga(self, manga: Manga) -> Manga:
        """Create a new manga in Firestore."""
        doc_ref = self._db.collection("mangas").document(manga.id)
        if doc_ref.get().exists:
            raise ValueError(f"Manga with id '{manga.id}' already exists")
        
        doc_ref.set({
            "title": manga.title,
            "description": manga.description,
            "cover_path": manga.cover_path,
            "recommended": manga.recommended,
            "tags": manga.tags,
        })
        logger.info(f"Created manga {manga.id}")
        return manga

    def list_chapters(self, manga_id: str) -> Iterable[Chapter]:
        col = self._db.collection("mangas").document(manga_id).collection("chapters")

        try:
            snaps = list(col.order_by("number").stream())
        except Exception as e:
            logger.warning("No se pudo order_by(number): %s", e)
            snaps = list(col.stream())

        for doc in snaps:
            data = doc.to_dict() or {}
            if data.get("number") is None:
                continue

            yield Chapter(
                id=doc.id,
                manga_id=(data.get("manga_id") or manga_id),
                number=int(data["number"]),
                pdf_path=data.get("pdf_path", "") or "",
                thumb_path=data.get("thumb_path", "") or "",
                title=data.get("title", "") or "",
            )

    def get_chapter_by_id(self, manga_id: str, chapter_id: str) -> Optional[Chapter]:
        snap = (
            self._db.collection("mangas")
            .document(manga_id)
            .collection("chapters")
            .document(chapter_id)
            .get()
        )
        if not snap.exists:
            return None
        data = snap.to_dict() or {}
        if data.get("number") is None:
            return None

        return Chapter(
            id=snap.id,
            manga_id=(data.get("manga_id") or manga_id),
            number=int(data["number"]),
            pdf_path=data.get("pdf_path", "") or "",
            thumb_path=data.get("thumb_path", "") or "",
            title=data.get("title", "") or "",
        )

    def get_chapter_by_number(self, manga_id: str, number: int) -> Optional[Chapter]:
        col = self._db.collection("mangas").document(manga_id).collection("chapters")
        snaps = list(col.where("number", "==", int(number)).limit(1).stream())
        if not snaps:
            return None

        doc = snaps[0]
        data = doc.to_dict() or {}
        return Chapter(
            id=doc.id,
            manga_id=(data.get("manga_id") or manga_id),
            number=int(data.get("number", number)),
            pdf_path=data.get("pdf_path", "") or "",
            thumb_path=data.get("thumb_path", "") or "",
            title=data.get("title", "") or "",
        )

    # compatibilidad si aún usas "episodes"
    def list_episodes(self, manga_id: str) -> Iterable[Chapter]:
        return self.list_chapters(manga_id)

    def get_episode_by_id(self, manga_id: str, episode_id: str) -> Optional[Chapter]:
        return self.get_chapter_by_id(manga_id, episode_id)

    def get_episode_by_number(self, manga_id: str, number: int) -> Optional[Chapter]:
        return self.get_chapter_by_number(manga_id, number)

    def create_chapter(self, chapter: Chapter) -> Chapter:
        """Create a new chapter in Firestore."""
        doc_ref = (
            self._db.collection("mangas")
            .document(chapter.manga_id)
            .collection("chapters")
            .document(chapter.id)
        )
        doc_ref.set({
            "manga_id": chapter.manga_id,
            "number": chapter.number,
            "title": chapter.title,
            "pdf_path": chapter.pdf_path,
            "thumb_path": chapter.thumb_path,
            "status": "pending_review",  # User uploads need review
        })
        logger.info(f"Created chapter {chapter.id} for manga {chapter.manga_id}")
        return chapter

