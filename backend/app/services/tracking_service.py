from collections import defaultdict

from app.models.tracking import (
    BoundingBox,
    Track,
    TrackHistory,
    TrackPoint,
)
from app.services.frame_service import FrameService
from app.services.image_service import ImageService
from app.services.yolo_service import YOLOService


class TrackingService:
    """
    Verarbeitet mehrere Frames und erstellt eine Track-Historie.
    """

    def __init__(
        self,
        frame_service: FrameService,
        image_service: ImageService,
        yolo_service: YOLOService,
    ):
        self.frame_service = frame_service
        self.image_service = image_service
        self.yolo_service = yolo_service

    def track_video(
        self,
        video_id: str,
        start_frame: int = 0,
        max_frames: int = 100,
    ) -> TrackHistory:

        frames = self.frame_service.list_frames(video_id)
        frames = frames[start_frame:start_frame + max_frames]

        history: dict[int, list[TrackPoint]] = defaultdict(list)

        for index, frame in enumerate(frames):

            frame_path = self.frame_service.get_frame(
                video_id,
                frame,
            )

            image = self.image_service.load_image(frame_path)

            tracks = self.yolo_service.track_people(image)

            for track in tracks:

                if track["track_id"] is None:
                    continue

                center_x = int(
                    (track["x1"] + track["x2"]) / 2
                )

                center_y = int(
                    (track["y1"] + track["y2"]) / 2
                )

                point = TrackPoint(
                    frame=start_frame + index,
                    frame_name=frame_path.name,
                    center_x=center_x,
                    center_y=center_y,
                    confidence=track["confidence"],
                    bbox=BoundingBox(
                        x1=track["x1"],
                        y1=track["y1"],
                        x2=track["x2"],
                        y2=track["y2"],
                    ),
                )

                history[track["track_id"]].append(point)

        track_list: list[Track] = []

        for track_id in sorted(history.keys()):
            track_list.append(
                Track(
                    track_id=track_id,
                    history=history[track_id],
                )
            )

        return TrackHistory(
            video_id=video_id,
            start_frame=start_frame,
            processed_frames=len(frames),
            track_count=len(track_list),
            tracks=track_list,
        )