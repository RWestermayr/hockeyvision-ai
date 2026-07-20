from pydantic import BaseModel, Field


class RinkPoint(BaseModel):
    x: float
    y: float


class RinkLine(BaseModel):
    start: RinkPoint
    end: RinkPoint

    length: float
    angle: float

    midpoint: RinkPoint

    classification: str = "unknown"


class RinkGeometry(BaseModel):
    image_width: int
    image_height: int

    lines: list[RinkLine] = Field(default_factory=list)

    board_lines: list[RinkLine] = Field(default_factory=list)

    blue_lines: list[RinkLine] = Field(default_factory=list)

    red_lines: list[RinkLine] = Field(default_factory=list)

    goal_lines: list[RinkLine] = Field(default_factory=list)

    reference_points: list[RinkPoint] = Field(default_factory=list)