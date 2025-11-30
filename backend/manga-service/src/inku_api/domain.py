from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any

class Manga(BaseModel):
    id: str
    title: str = ""
    description: str = ""
    cover_path: str = ""
    recommended: Optional[str] = None  # en tu captura es texto
    tags: List[str] = Field(default_factory=list)

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v: Any):
        # Acepta array o string "a, b, c"
        if v is None:
            return []
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        return []

class Chapter(BaseModel):
    id: str
    manga_id: str
    number: int
    pdf_path: str = ""
    thumb_path: str = ""
    title: str = ""
