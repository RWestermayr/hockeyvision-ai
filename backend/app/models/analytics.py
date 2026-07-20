from pydantic import BaseModel


class PlayerAnalytics(BaseModel):
    track_id: int
    distance: float
    average_speed: float
    max_speed: float
    time_on_ice: float
    track_points: int


class AnalyticsResult(BaseModel):
    video_id: str
    player_count: int
    players: list[PlayerAnalytics]