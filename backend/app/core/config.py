from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Projektstamm: hockeyvision-ai/
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "HockeyVision AI"
    app_version: str = "0.1.0"
    debug: bool = True

    upload_dir: str = "data/uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def upload_path(self) -> Path:
        return BASE_DIR / self.upload_dir


settings = Settings()