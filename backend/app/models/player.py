from pydantic import BaseModel, Field

from app.models.tracking import Track


class Player(BaseModel):
    """
    Repräsentiert einen Spieler im Spiel.
    """

    track_id: int

    team: str | None = None

    jersey_number: int | None = None

    position: str | None = None

    average_speed: float = Field(default=0.0, ge=0.0)

    max_speed: float = Field(default=0.0, ge=0.0)

    distance: float = Field(default=0.0, ge=0.0)

    time_on_ice: float = Field(default=0.0, ge=0.0)

    track: Track