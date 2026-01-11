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

    def presign(self, key: str, expires: int = None, content_type: str = None, inline: bool = True) -> str:
        """Devuelve una URL firmada temporal (GET) para el objeto `key`.
        
        Args:
            key: S3 object key
            expires: URL expiration in seconds (uses default if not specified)
            content_type: Force response content type (e.g., 'application/pdf')
            inline: If True, force inline display (not download)
        """
        exp = expires or self._expires
        
        params = {"Bucket": self._bucket, "Key": key}
        
        # Force content type for PDF files
        if content_type:
            params["ResponseContentType"] = content_type
        elif key.endswith(".pdf"):
            params["ResponseContentType"] = "application/pdf"
        
        # Force inline display
        if inline:
            filename = key.split("/")[-1]
            params["ResponseContentDisposition"] = f"inline; filename=\"{filename}\""
        
        return self._client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=exp,
        )
