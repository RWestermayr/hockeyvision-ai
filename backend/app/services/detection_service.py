from app.models.detection import (
    BoundingBox,
    Detection,
    DetectionResult,
)
from app.services.frame_service import FrameService
from app.services.image_service import ImageService
from app.services.yolo_service import YOLOService


class DetectionService:
    """
    Führt Personenerkennung auf einem einzelnen Frame aus und
    liefert ein typisiertes DetectionResult zurück.
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

    def detect_frame(
        self,
        video_id: str,
        frame_name: str,
    ) -> DetectionResult:

        frame_path = self.frame_service.get_frame(
            video_id,
            frame_name,
        )

        if frame_path is None:
            raise FileNotFoundError(
                f"Frame '{frame_name}' not found."
            )

        image = self.image_service.load_image(frame_path)

        raw_detections = self.yolo_service.detect_people(image)

        detections: list[Detection] = []

        for detection in raw_detections:

            detections.append(
                Detection(
                    class_id=detection["class_id"],
                    class_name=detection["class_name"],
                    confidence=detection["confidence"],
                    bbox=BoundingBox(
                        x1=detection["x1"],
                        y1=detection["y1"],
                        x2=detection["x2"],
                        y2=detection["y2"],
                    ),
                )
            )

        return DetectionResult(
            video_id=video_id,
            frame_name=frame_name,
            count=len(detections),
            detections=detections,
        )