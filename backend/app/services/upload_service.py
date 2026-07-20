from pathlib import Path
import shutil
import uuid

from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.services.video_service import VideoService


class UploadService:
    """Service for saving uploaded video files."""

    def __init__(self):
        self.upload_dir = settings.upload_path
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        self.video_service = VideoService()

    def save_video(self, file: UploadFile) -> dict:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No filename provided.",
            )

        extension = Path(file.filename).suffix.lower()

        allowed_extensions = {
            ".mp4",
            ".mov",
            ".avi",
            ".mkv",
        }

        if extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {extension}",
            )

        video_id = str(uuid.uuid4())
        stored_filename = f"{video_id}{extension}"

        destination = self.upload_dir / stored_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        video_info = self.video_service.get_video_info(destination)

        return {
            "video_id": video_id,
            "video_path": destination,
            "video": video_info,
        }