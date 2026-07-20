import random
from pathlib import Path

from app.core.config import settings


class FrameService:
    def get_video_frame_directory(self, video_id: str) -> Path:
        return settings.frames_path / video_id

    def list_frames(self, video_id: str) -> list[Path]:
        frame_directory = self.get_video_frame_directory(video_id)

        if not frame_directory.exists():
            return []

        return sorted(frame_directory.glob("*.jpg"))

    def get_frame_count(self, video_id: str) -> int:
        return len(self.list_frames(video_id))

    def get_first_frame(self, video_id: str) -> Path | None:
        frames = self.list_frames(video_id)

        if not frames:
            return None

        return frames[0]

    def get_random_frame(self, video_id: str) -> Path | None:
        frames = self.list_frames(video_id)

        if not frames:
            return None

        return random.choice(frames)

    def get_frame(self, video_id: str, frame_name: str) -> Path | None:
        frame = self.get_video_frame_directory(video_id) / frame_name

        if frame.exists():
            return frame

        return None