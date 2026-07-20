from fastapi import APIRouter, File, UploadFile

from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter()

upload_service = UploadService()


@router.get("/")
def root():
    return {"message": "Welcome to HockeyVision AI"}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/upload", response_model=UploadResponse)
async def upload_video(file: UploadFile = File(...)):
    return upload_service.save_video(file)