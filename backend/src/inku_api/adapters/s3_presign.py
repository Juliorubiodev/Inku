import logging
import boto3
from botocore.config import Config

from ..config import settings


class Boto3S3Presign:
    """
    Firma URLs de S3 (GET) con boto3 usando la configuración de `settings`.
    Requiere:
      - settings.aws_region
      - settings.aws_access_key_id
      - settings.aws_secret_access_key
      - settings.s3_bucket_name
      - settings.s3_presign_expires_seconds
    """

    def __init__(self) -> None:
        self._bucket = settings.s3_bucket_name
        self._expires = settings.s3_presign_expires_seconds

        self._client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        logging.info(
            "S3 presign listo (bucket=%s, region=%s) | {}",
            self._bucket,
            settings.aws_region,
        )

    def presign(self, key: str) -> str:
        """Devuelve una URL firmada temporal (GET) para el objeto `key`."""
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": key},
            ExpiresIn=self._expires,
        )
