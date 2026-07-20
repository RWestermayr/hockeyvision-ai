from pydantic import BaseModel


class VideoInfo(BaseModel):
    filename: str
    size_bytes: int


class UploadResponse(BaseModel):
    id: str
    original_filename: str
    stored_filename: str
    content_type: str
    saved_to: str
    video: VideoInfo