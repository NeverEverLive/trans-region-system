import logging
import uuid

from fastapi import APIRouter, UploadFile, Body

from src.schemas.project import ProjectResponseSchema, ProjectsResponseSchema, ProjectSchema
from src.schemas.filter import FilterSchema
from src.pipelines.project import create, update, get_all, get, delete, get_image


router = APIRouter()


@router.post(
    "",
    response_model=ProjectResponseSchema,
    status_code=201,
)
async def create_project_endpoint(
    project: ProjectSchema = Body(), 
    preview: UploadFile | None = None,
):
    return await create(project, preview)


@router.post(
    "/filter",
    response_model=ProjectsResponseSchema,
    status_code=200
)
async def get_cities_endpoint(filters: FilterSchema):
    return get_all(filters)


@router.get(
    "{_id}",
    response_model=ProjectResponseSchema,
    status_code=200
)
def get_project_endpoint(_id: uuid.UUID):
    return get(_id)


@router.get(
    "/image",
    response_model=ProjectResponseSchema,
    status_code=200
)
def get_project_image_endpoint(path: str):
    return get_image(path)


@router.put(
    "", 
    response_model=ProjectResponseSchema,
    status_code=200
)
async def update_project_endpoint(
    project: ProjectSchema, 
    preview: UploadFile | None = None,

):
    return await update(project, preview)


@router.delete(
    "{_id}",
    response_model=ProjectResponseSchema,
    status_code=202
)
async def delete_project_endpoint(_id: uuid.UUID):
    return await delete(_id)
