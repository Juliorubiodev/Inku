from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    api_prefix: str = Field("/api", alias="API_PREFIX")
    debug: bool = Field(default=True, alias="DEBUG")

    firebase_project_id: str = Field(alias="FIREBASE_PROJECT_ID")
    firebase_cred_file: str = Field(
        validation_alias=AliasChoices(
            "FIREBASE_CRED_FILE",
            "FIREBASE_SERVICE_ACCOUNT_FILE",
            "GOOGLE_APPLICATION_CREDENTIALS",
        )
    )

    # AWS opcional
    aws_region: Optional[str] = Field(default=None, alias="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    s3_bucket_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("S3_BUCKET_NAME", "AWS_S3_BUCKET", "S3_BUCKET")
    )
    s3_presign_expires_seconds: int = Field(default=900, alias="S3_PRESIGN_EXPIRES_SECONDS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()
