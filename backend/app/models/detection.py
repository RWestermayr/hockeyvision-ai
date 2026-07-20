from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class Detection(BaseModel):
    class_id: int

    class_name: str

    confidence: float = Field(..., ge=0.0, le=1.0)

    bbox: BoundingBox


class DetectionResult(BaseModel):
    video_id: str

    frame_name: str

    count: int

    detections: list[Detection] = Field(default_factory=list)