from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel

class Episode(BaseModel):
    id: str
    manga_id: str
    number: Optional[int] = None
    title: Optional[str] = None
    s3_key: Optional[str] = None

class Manga(BaseModel):
    id: str
    title: Optional[str] = None
    cover_url: Optional[str] = None
    episodes: Optional[List[Episode]] = None
