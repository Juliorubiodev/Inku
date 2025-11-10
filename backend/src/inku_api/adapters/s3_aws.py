from __future__ import annotations
import logging
import boto3
from botocore.client import Config
from ..config import settings

logger = logging.getLogger(__name__)

class Boto3S3Presign:
    def __init__(self):
        session = boto3.session.Session(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
        self._s3 = session.client("s3", config=Config(signature_version="s3v4"))
        self._bucket = settings.s3_bucket_name
        logger.info(
            "S3 presign listo (bucket=%s, region=%s)", self._bucket, settings.aws_region
        )

    def presign_get(self, key: str, expires: int = None) -> str:
        exp = expires or settings.s3_presign_expires_seconds
        return self._s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=exp,
        )
