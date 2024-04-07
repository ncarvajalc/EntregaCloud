import os
from enum import Enum
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class ModeEnum(str, Enum):
    development = "development"
    production = "production"


class Settings(BaseSettings):
    PROJECT_NAME: str = "app"
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    MODE: ModeEnum = ModeEnum.development
    DATABASE_URL: str = "sqlite:///:memory:"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    SHARED_VOLUME_PATH: str = "/uploads"

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("~/.env")


settings = Settings()
