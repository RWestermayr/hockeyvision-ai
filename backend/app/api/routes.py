from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.models.analytics import AnalyticsResult
from app.models.detection import DetectionResult
from app.models.tracking import TrackHistory
from app.services.analytics_service import AnalyticsService
from app.services.detection_service import DetectionService
from app.services.frame_service import FrameService
from app.services.image_service import ImageService
from app.services.job_service import JobService
from app.services.pipeline_service import PipelineService
from app.services.player_service import PlayerService
from app.services.tracking_service import TrackingService
from app.services.upload_service import UploadService
from app.services.yolo_service import YOLOService

router = APIRouter()

frame_service = FrameService()
job_service = JobService()

upload_service = UploadService()

pipeline_service = PipelineService(
    frame_service=frame_service,
    job_service=job_service,
)

image_service = ImageService()
yolo_service = YOLOService()

detection_service = DetectionService(
    frame_service=frame_service,
    image_service=image_service,
    yolo_service=yolo_service,
)

tracking_service = TrackingService(
    frame_service=frame_service,
    image_service=image_service,
    yolo_service=yolo_service,
)

player_service = PlayerService()

analytics_service = AnalyticsService()


@router.get("/")
def root():
    return {
        "message": "HockeyVision AI API",
    }


@router.get("/health")
def health():
    return {
        "status": "ok",
    }


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    upload = upload_service.save_video(file)

    pipeline_service.process_video(
        video_id=upload["video_id"],
        video_path=upload["video_path"],
    )

    return {
        "message": "Upload successful.",
        "video_id": upload["video_id"],
        "video": upload["video"],
    }


@router.get("/jobs/{video_id}")
def get_job(video_id: str):
    return job_service.get_job(video_id)


@router.get("/videos/{video_id}/frames")
def list_frames(video_id: str):
    frames = frame_service.list_frames(video_id)

    return {
        "video_id": video_id,
        "frame_count": len(frames),
        "frames": frames,
    }


@router.get(
    "/videos/{video_id}/frames/{frame_name}/detect",
    response_model=DetectionResult,
)
def detect_frame(
    video_id: str,
    frame_name: str,
) -> DetectionResult:

    try:
        return detection_service.detect_frame(
            video_id=video_id,
            frame_name=frame_name,
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Frame not found.",
        )


@router.get("/videos/{video_id}/frames/{frame_name}/track")
def track_frame(video_id: str, frame_name: str):

    frame_path = frame_service.get_frame(video_id, frame_name)

    if frame_path is None:
        raise HTTPException(
            status_code=404,
            detail="Frame not found.",
        )

    image = image_service.load_image(frame_path)

    tracks = yolo_service.track_people(image)

    return {
        "video_id": video_id,
        "frame": frame_name,
        "count": len(tracks),
        "tracks": tracks,
    }


@router.get("/videos/{video_id}/frames/{frame_name}/image")
def detect_image(video_id: str, frame_name: str):

    frame_path = frame_service.get_frame(video_id, frame_name)

    if frame_path is None:
        raise HTTPException(
            status_code=404,
            detail="Frame not found.",
        )

    image = image_service.load_image(frame_path)

    annotated = yolo_service.detect_and_draw(image)

    output_path = settings.output_path / f"{video_id}_{frame_name}"

    image_service.save_image(
        output_path,
        annotated,
    )

    return {
        "message": "Detection image created.",
        "saved_to": str(output_path),
    }


@router.get("/videos/{video_id}/frames/{frame_name}/track-image")
def track_image(video_id: str, frame_name: str):

    frame_path = frame_service.get_frame(video_id, frame_name)

    if frame_path is None:
        raise HTTPException(
            status_code=404,
            detail="Frame not found.",
        )

    image = image_service.load_image(frame_path)

    annotated = yolo_service.track_and_draw(image)

    output_path = settings.output_path / f"{video_id}_tracked_{frame_name}"

    image_service.save_image(
        output_path,
        annotated,
    )

    return {
        "message": "Tracking image created.",
        "saved_to": str(output_path),
    }


@router.get(
    "/videos/{video_id}/tracks",
    response_model=TrackHistory,
)
def track_video(
    video_id: str,
    start_frame: int = 0,
    max_frames: int = 100,
) -> TrackHistory:

    return tracking_service.track_video(
        video_id=video_id,
        start_frame=start_frame,
        max_frames=max_frames,
    )


@router.get(
    "/videos/{video_id}/analytics",
    response_model=AnalyticsResult,
)
def analytics(
    video_id: str,
    start_frame: int = 0,
    max_frames: int = 100,
) -> AnalyticsResult:

    history = tracking_service.track_video(
        video_id=video_id,
        start_frame=start_frame,
        max_frames=max_frames,
    )

    players = player_service.create_players(history)

    return analytics_service.analyze_players(
        players=players,
        video_id=video_id,
    )