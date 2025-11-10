from __future__ import annotations
import logging
from typing import Iterable, Optional, List

import firebase_admin
from firebase_admin import credentials, firestore

from ..config import settings
from ..domain import Episode
from ..ports import MangaRepository

logger = logging.getLogger(__name__)

_initialized = False

def _ensure_init():
    global _initialized
    if _initialized:
        return
    cred = credentials.Certificate(settings.firebase_cred_file)
    firebase_admin.initialize_app(cred, {"projectId": settings.firebase_project_id})
    _initialized = True
    logger.info("Firebase inicializado (project_id=%s)", settings.firebase_project_id)

def _map_episode(manga_id: str, doc) -> Episode:
    data = doc.to_dict() or {}
    return Episode(
        id=doc.id,
        manga_id=manga_id,
        number=data.get("number"),
        title=data.get("title"),
        # Acepta variantes de nombre de campo
        s3_key=data.get("s3_key") or data.get("s3Key") or data.get("s3-path"),
    )

class _FirestorePaths:
    # Fallbacks por si tu top collection o subcollection tienen otro nombre
    TOPS = ["mangas", "manga"]
    SUBS = ["episodes", "chapters", "capitulos"]

class FirestoreMangaRepo(MangaRepository):
    def __init__(self):
        _ensure_init()
        self._db = firestore.client()

    # ---- Nuevo: lista IDs de mangas (primer nivel)
    def list_mangas(self) -> Iterable[str]:
        # Probamos "mangas" y "manga"
        seen = set()
        for top in _FirestorePaths.TOPS:
            for doc in self._db.collection(top).stream():
                if doc.id not in seen:
                    seen.add(doc.id)
                    yield doc.id

    def _episode_collection_candidates(self, manga_id: str):
        # Genera todas las combinaciones top/sub para buscar episodios
        for top in _FirestorePaths.TOPS:
            parent = self._db.collection(top).document(manga_id)
            for sub in _FirestorePaths.SUBS:
                yield parent.collection(sub), f"{top}/{manga_id}/{sub}"

    def list_episodes(self, manga_id: str) -> Iterable[Episode]:
        found_any = False
        # Buscamos en varias rutas posibles y unimos resultados por orden
        for col, path in self._episode_collection_candidates(manga_id):
            try:
                # Si tienen 'number' lo ordenamos, si no, stream tal cual
                try:
                    q = col.order_by("number")
                    snaps = list(q.stream())
                except Exception:
                    snaps = list(col.stream())
                if snaps:
                    found_any = True
                    logger.info("Firestore: episodios encontrados en '%s' (count=%d)", path, len(snaps))
                    for doc in snaps:
                        yield _map_episode(manga_id, doc)
            except Exception as e:
                logger.warning("Firestore: error leyendo '%s': %s", path, e)

        if not found_any:
            logger.info("Firestore: no se encontraron episodios para '%s' en ninguno de los paths", manga_id)

    def get_episode_by_id(self, manga_id: str, episode_id: str) -> Optional[Episode]:
        for col, path in self._episode_collection_candidates(manga_id):
            try:
                snap = col.document(episode_id).get()
                if snap.exists:
                    logger.info("Firestore: episodio '%s' encontrado en '%s'", episode_id, path)
                    return _map_episode(manga_id, snap)
            except Exception as e:
                logger.warning("Firestore: error en get_by_id '%s' en '%s': %s", episode_id, path, e)
        return None

    def get_episode_by_number(self, manga_id: str, number: int) -> Optional[Episode]:
        for col, path in self._episode_collection_candidates(manga_id):
            try:
                q = col.where("number", "==", int(number)).limit(1)
                snaps = list(q.stream())
                if snaps:
                    logger.info("Firestore: episodio number=%s encontrado en '%s'", number, path)
                    return _map_episode(manga_id, snaps[0])
            except Exception as e:
                logger.warning("Firestore: error en get_by_number %s en '%s': %s", number, path, e)
        return None
