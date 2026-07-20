from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "HockeyVision AI"

    upload_dir: str = "data/uploads"
    frames_dir: str = "data/frames"
    output_dir: str = "data/output"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def upload_path(self) -> Path:
        return BASE_DIR / self.upload_dir

    @property
    def frames_path(self) -> Path:
        return BASE_DIR / self.frames_dir

    @property
    def output_path(self) -> Path:
        return BASE_DIR / self.output_dir


settings = Settings()