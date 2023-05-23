import logging
import uuid

from fastapi import APIRouter, UploadFile, Body

from src.schemas.project import ProjectResponseSchema, ProjectSchema, ProjectsResponseSchema
from src.pipelines.project import create, update, get_all, get, delete, get_preview


router = APIRouter()


@router.post(
    "",
    response_model=ProjectResponseSchema,
    status_code=201,
)
async def create_project_endpoint(project: ProjectSchema = Body(), preview: UploadFile | None = None):
    return await create(project, preview)


@router.get(
    "",
    response_model=ProjectsResponseSchema,
    status_code=200
)
def get_cities_endpoint():
    return get_all()


@router.get(
    "{_id}",
    response_model=ProjectResponseSchema,
    status_code=200
)
def get_project_endpoint(_id: uuid.UUID):
    return get(_id)


@router.get(
    "/preview",
    response_model=ProjectResponseSchema,
    status_code=200
)
def get_project_preview_endpoint(path: str):
    return get_preview(path)


@router.put(
    "", 
    response_model=ProjectResponseSchema,
    status_code=200
)
async def update_project_endpoint(project: ProjectSchema, preview: UploadFile):
    return await update(project, preview)


@router.delete(
    "{_id}",
    response_model=ProjectResponseSchema,
    status_code=202
)
async def delete_project_endpoint(_id: uuid.UUID):
    return delete(_id)
