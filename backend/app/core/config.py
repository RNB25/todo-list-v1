import os
from pathlib import Path
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Dynamically locate backend/.env and root .env
_current_dir = Path(__file__).resolve().parent
_backend_dir = _current_dir.parent.parent
_env_files = [
    str(_backend_dir / ".env"),
    str(_backend_dir.parent / ".env"),
    ".env"
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_files,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = "mysql+pymysql://root:@127.0.0.1:3306/todo_db"

    CORS_ORIGINS: Union[List[str], str] = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"

    API_V1_PREFIX: str = "/api/v1"
    PAGE_SIZE_DEFAULT: int = 20
    PAGE_SIZE_MAX: int = 100
    BULK_COUNT_DEFAULT: int = 1000
    BULK_COUNT_MAX: int = 1000

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v


settings = Settings()
