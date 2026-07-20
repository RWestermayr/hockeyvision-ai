from pathlib import Path

from app.services.frame_service import FrameService
from app.services.job_service import JobService


class PipelineService:
    """Service for processing uploaded videos."""

    def __init__(
        self,
        frame_service: FrameService,
        job_service: JobService,
    ):
        self.frame_service = frame_service
        self.job_service = job_service

    def process_video(
        self,
        video_id: str,
        video_path: Path,
    ) -> None:
        try:
            self.job_service.update_status(
                video_id,
                "extracting_frames",
            )

            self.frame_service.extract_frames(video_path)

            self.job_service.update_status(
                video_id,
                "completed",
            )

        except Exception:
            self.job_service.update_status(
                video_id,
                "failed",
            )