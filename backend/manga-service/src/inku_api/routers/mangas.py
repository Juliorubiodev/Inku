from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from firebase_admin import firestore as admin_firestore

from ..firebase_app import init_firebase
from ..services.manga_services import MangaService
from ..adapters.repo_firebase import FirestoreMangaRepo
from ..domain import Manga, Chapter

router = APIRouter(prefix="/mangas", tags=["mangas"])

def get_service() -> MangaService:
    init_firebase()
    db = admin_firestore.client()
    repo = FirestoreMangaRepo(db)
    return MangaService(repo)

@router.get("", response_model=List[Manga])
def list_mangas(svc: MangaService = Depends(get_service)) -> List[Manga]:
    return svc.list_mangas()

@router.get("/{manga_id}/chapters", response_model=List[Chapter])
def list_chapters(manga_id: str, svc: MangaService = Depends(get_service)) -> List[Chapter]:
    try:
        return svc.list_chapters(manga_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="MANGA_NOT_FOUND")
