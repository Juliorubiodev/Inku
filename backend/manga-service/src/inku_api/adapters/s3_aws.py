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

    def presign_get(self, key: str, expires: int = None, content_type: str = None, inline: bool = True) -> str:
        """Generate presigned URL for downloading (GET).
        
        Args:
            key: S3 object key
            expires: URL expiration in seconds
            content_type: Force response content type (e.g., 'application/pdf')
            inline: If True, force inline display (not download)
        """
        exp = expires or settings.s3_presign_expires_seconds
        
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
        
        return self._s3.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=exp,
        )

    def presign_put(self, key: str, content_type: str = "application/pdf", expires: int = None) -> str:
        """Generate presigned URL for uploading (PUT)."""
        exp = expires or settings.s3_presign_expires_seconds
        return self._s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": self._bucket,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=exp,
        )

