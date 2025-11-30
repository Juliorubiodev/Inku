from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional, List, Union
from ..domain import Chapter, Manga
from ..ports import MangaRepository, S3PresignService

@dataclass
class MangaService:
    repo: MangaRepository
    s3: S3PresignService

    def __init__(self, repo):
        self.repo = repo

    # ---- Nuevo: listar mangas (IDs)
    def list_mangas(self) -> List[Manga]:
        return list(self.repo.list_mangas())

    def list_chapters(self, manga_id: str) -> List[Chapter]:
        if not self.repo.manga_exists(manga_id):
            raise KeyError("MANGA_NOT_FOUND")
        return list(self.repo.list_chapters(manga_id))

    def get_episode(self, manga_id: str, ident: Union[str,int]) -> Optional[Chapter]:
        if isinstance(ident, int) or (isinstance(ident, str) and ident.isdigit()):
            return self.repo.get_episode_by_number(manga_id, int(ident))
        else:
            return self.repo.get_episode_by_id(manga_id, ident)

    def presign_read(self, ep: Chapter, expires: int = 900) -> str:
        if not ep.s3_key:
            raise ValueError("El episodio no tiene 's3_key' definido")
        return self.s3.presign_get(ep.s3_key, expires=expires)
