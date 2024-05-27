import os
from enum import Enum
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class ModeEnum(str, Enum):
    development = "development"
    production = "production"


class Settings(BaseSettings):
    PROJECT_NAME: str = "app"
    MODE: ModeEnum = ModeEnum.development
    DATABASE_URL: str = "sqlite:///:memory:"
    SHARED_VOLUME_PATH: str = "/uploads"
    HOST: str = "http://localhost"
    GCP_BUCKET_NAME: str = "app"
    GOOGLE_CLOUD_PROJECT: str = "project_id"

    class Config:
        case_sensitive = True


settings = Settings()
