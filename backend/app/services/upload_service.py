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
        allowed_extensions = {".mp4", ".mov", ".avi", ".mkv"}

        extension = Path(file.filename).suffix.lower()

        if extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type.",
            )

        file_id = uuid.uuid4()
        stored_filename = f"{file_id}{extension}"

        destination = self.upload_dir / stored_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        video_info = self.video_service.get_video_info(destination)

        return {
            "id": str(file_id),
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "content_type": file.content_type,
            "saved_to": str(destination),
            "video": video_info,
        }