import logging

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.pipelines.project import get_image


router = APIRouter()

@router.get(
    "/image",
    response_class=FileResponse,
    status_code=200
)
def get_project_image_endpoint(path: str):
    """Эндпоинт для получения картинки"""
    return get_image(path)
