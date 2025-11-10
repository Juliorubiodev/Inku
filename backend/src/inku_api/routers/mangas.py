from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..services.manga_services import MangaService
from ..adapters.repo_firebase import FirestoreMangaRepo
from ..adapters.s3_aws import Boto3S3Presign

router = APIRouter(prefix="/mangas", tags=["mangas"])

def get_service() -> MangaService:
    return MangaService(repo=FirestoreMangaRepo(), s3=Boto3S3Presign())

# ---- Nuevo: listar mangas disponibles (IDs de documentos de primer nivel)
@router.get("")
def list_mangas(svc: MangaService = Depends(get_service)) -> List[str]:
    return svc.list_mangas()

@router.get("/{manga_id}/episodes")
def list_episodes(manga_id: str, svc: MangaService = Depends(get_service)) -> List[dict]:
    eps = [e.model_dump() for e in svc.list_episodes(manga_id)]
    # Ya NO devolvemos 404; regresamos lista (posiblemente vacía)
    return eps

@router.get("/{manga_id}/episodes/{episode_id}/read")
def read_episode(manga_id: str, episode_id: str, svc: MangaService = Depends(get_service)) -> dict:
    ep = svc.get_episode(manga_id, episode_id)
    if not ep:
        raise HTTPException(status_code=404, detail=f"Episodio '{episode_id}' no encontrado para manga '{manga_id}'")
    try:
        url = svc.presign_read(ep)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    return {"url": url}
