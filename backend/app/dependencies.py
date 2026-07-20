from app.services.frame_service import FrameService
from app.services.image_service import ImageService
from app.services.job_service import JobService
from app.services.pipeline_service import PipelineService
from app.services.upload_service import UploadService
from app.services.video_service import VideoService
from app.services.yolo_service import YOLOService

job_service = JobService()

video_service = VideoService()

frame_service = FrameService()

image_service = ImageService()

yolo_service = YOLOService()

upload_service = UploadService()

pipeline_service = PipelineService(
    frame_service=frame_service,
    job_service=job_service,
)