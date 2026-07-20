from pydantic import BaseModel


class JobResponse(BaseModel):
    video_id: str
    status: str