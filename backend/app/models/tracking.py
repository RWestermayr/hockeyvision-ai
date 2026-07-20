from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class TrackPoint(BaseModel):
    frame: int
    frame_name: str

    center_x: int
    center_y: int

    confidence: float = Field(..., ge=0.0, le=1.0)

    bbox: BoundingBox


class Track(BaseModel):
    track_id: int

    history: list[TrackPoint] = Field(default_factory=list)


class TrackHistory(BaseModel):
    video_id: str

    start_frame: int

    processed_frames: int

    track_count: int

    tracks: list[Track] = Field(default_factory=list)