from pydantic import BaseModel


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

    confidence: float

    bbox: BoundingBox


class Track(BaseModel):
    track_id: int

    history: list[TrackPoint]


class TrackHistory(BaseModel):
    video_id: str

    start_frame: int

    processed_frames: int

    track_count: int

    tracks: list[Track]