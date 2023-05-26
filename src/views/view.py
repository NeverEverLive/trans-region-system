import logging

from fastapi import APIRouter, UploadFile

from src.pipelines.project import get_image


router = APIRouter()

@router.get(
    "/image",
    response_model=UploadFile,
    status_code=200
)
def get_project_image_endpoint(path: str):
    logging.warning(path)
    return get_image(path)
