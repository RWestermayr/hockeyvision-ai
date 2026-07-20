from pydantic import BaseModel


class VideoInfo(BaseModel):
    filename: str
    size_bytes: int
    duration_seconds: float
    fps: float
    width: int
    height: int
    codec: str


class UploadResponse(BaseModel):
    video_id: str
    status: str
    video: VideoInfo