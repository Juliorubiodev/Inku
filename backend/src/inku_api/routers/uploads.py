from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..services.manga_services import MangaService


class CreateEpisodeIn(BaseModel):
    episode_id: str
    number: int


def get_service() -> MangaService:
    from ..adapters.repo_firebase import FirestoreMangaRepo
    from ..adapters.s3_aws import Boto3S3Presign

    return MangaService(repo=FirestoreMangaRepo(), s3=Boto3S3Presign())


router = APIRouter(prefix="/mangas", tags=["uploads"])


@router.post("/{manga_id}/episodes")
def create_episode(manga_id: str, body: CreateEpisodeIn, svc: MangaService = Depends(get_service)):
    urls = svc.create_episode_with_presign(
        manga_id=manga_id, episode_id=body.episode_id, number=body.number
    )
    return {"manga_id": manga_id, "episode_id": body.episode_id, **urls}
