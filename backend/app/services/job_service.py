from threading import Lock


class JobService:
    """Service for managing background processing jobs."""

    def __init__(self):
        self._jobs = {}
        self._lock = Lock()

    def create_job(self, video_id: str):
        with self._lock:
            self._jobs[video_id] = {
                "video_id": video_id,
                "status": "uploaded",
            }

    def update_status(self, video_id: str, status: str):
        with self._lock:
            if video_id in self._jobs:
                self._jobs[video_id]["status"] = status

    def get_job(self, video_id: str):
        with self._lock:
            return self._jobs.get(video_id)