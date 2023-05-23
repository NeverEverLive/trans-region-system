import logging
import uuid
from pathlib import Path

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from pydantic import parse_obj_as

from src.exceptions.project import ProjectException, ProjectDeleteException
from src.models.base import get_session
from src.models.project import Project
from src.schemas.project import ProjectSchema, ProjectResponseSchema, ProjectsResponseSchema
from src.settings import image_settings

async def create(project: ProjectSchema, preview: UploadFile):
    if preview:
        await upload_preview()
        project.preview = image_settings.get_url(preview.filename)

    project_state = Project().fill(**project.dict())

    with get_session() as session:
        session.add(project_state)
        session.commit()

        return ProjectResponseSchema(
            data=ProjectSchema.from_orm(project_state), 
            message="Project created", 
            success=True
        )


def get_all():
    return ProjectsResponseSchema(
        data=parse_obj_as(list[ProjectSchema], Project.all()),
        message="Cities accessed",
        success=True
    )


def get(_id: uuid.UUID):
    query = select(
        Project
    ).where(
        Project.id == _id
    ).limit(1)

    with get_session() as session:
        project = session.execute(query).scalar()
    
    if not project:
        raise ProjectException(
            status_code=400,
            message="Project not found"
        )

    return ProjectResponseSchema(
        data=project,
        message="Project accessed",
        success=True
    )


def get_preview(path: str):
    response = FileResponse(
        path=Path("preview_smb", path.replace("%", "/")),
        media_type="image/webp",
        filename=path.split("/")[-1],
    )
    response.direct_passthrough = False
    return response


async def upload_preview(preview: UploadFile):
    with open(image_settings.get_url(preview.filename), "wb") as image:
        image.write(await preview.read())


async def update(project: ProjectSchema, preview: UploadFile):
    if preview:
        await upload_preview()
        project.preview = image_settings.get_url(preview.filename)

    project_state = Project().fill(**project.dict())

    with get_session() as session:
        session.merge(project_state)
        session.commit()

    return ProjectResponseSchema(
        data=ProjectSchema.from_orm(project_state),
        message="Project updated",
        success=True
    )


def delete(_id: uuid.UUID):
    query = select(
        Project
    ).where(
        Project.id == _id
    ).limit(1)

    with get_session() as session:
        project = session.execute(query).scalar()

        if not project:
            raise ProjectDeleteException(
                status_code=404,
                message="Project not found"
            )

        session.delete(project)
        session.commit()

        return ProjectResponseSchema(data=project, message="Project deleted", success=True)
