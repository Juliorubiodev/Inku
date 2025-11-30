from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    FIREBASE_SERVICE_ACCOUNT_PATH: str
    FIREBASE_WEB_API_KEY: str
    SERVICE_NAME: str = "auth-service"
    API_PREFIX: str = "/api"

settings = Settings()
