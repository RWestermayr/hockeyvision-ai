from pathlib import Path


class VideoService:
    """Service für die Verarbeitung von Videos."""

    def get_video_info(self, video_path: Path) -> dict:
        return {
            "filename": video_path.name,
            "size_bytes": video_path.stat().st_size,
        }