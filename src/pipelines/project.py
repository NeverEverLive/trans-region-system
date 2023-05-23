import logging
import uuid
from pathlib import Path

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select, delete as sql_delete
from pydantic import parse_obj_as

from src.exceptions.project import ProjectException, ProjectDeleteException
from src.models.base import get_session
from src.models.project import Project
from src.models.image_project import ImageProject
from src.schemas.project import ProjectSchema, ProjectResponseSchema, ProjectsResponseSchema
from src.schemas.image_project import ImageProjectSchema
from src.settings import image_settings


async def create(project: ProjectSchema, preview: UploadFile, images: list[UploadFile]):
    if preview:
        await upload_preview(preview)
        project.preview = image_settings.get_url(preview.filename)

    images_queries = []
    if images:
        images_queries = await upload_images(project, images)

    project_state = Project().fill(**project.dict())

    with get_session() as session:
        session.add(project_state)
        for query in images_queries:
            session.add(query)
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
        project: Project = session.execute(query).scalar()

        if not project:
            raise ProjectException(
                status_code=400,
                message="Project not found"
            )

        images = []
        for image in project.images:
            logging.warning(image.path)
            images.append(image.path)
    project.images = []


    logging.warning({**ProjectSchema.from_orm(project).dict(exclude={"images"}), "images": images})

    return ProjectResponseSchema(
        data={**ProjectSchema.from_orm(project).dict(), "images": images},
        message="Project accessed",
        success=True
    )


def get_image(path: str):
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


async def upload_images(project: ProjectSchema, images: list[UploadFile]):
    with get_session() as session:
        query = sql_delete(
            ImageProject
        ).where(
            ImageProject.project_id == project.id
        )

        queries = []
        for image in images:
            queries.append(ImageProject().fill(**ImageProjectSchema.parse_obj({
                "project_id": project.id,
                "path": image_settings.get_url(image.filename),
            }).dict()))
            with open(image_settings.get_url(image.filename), "wb") as file:
                file.write(await image.read())

        session.execute(query)
        session.commit()

    return queries


async def update(project: ProjectSchema, preview: UploadFile, images: list[UploadFile]):
    logging.warning(preview)

    if preview:
        await upload_preview(preview)
        project.preview = image_settings.get_url(preview.filename)

    images_queries = []
    if images:
        images_queries = await upload_images(project, images)

    project_state = Project().fill(**project.dict())

    with get_session() as session:
        session.merge(project_state)
        for query in images_queries:
            session.add(query)
        session.commit()

    return ProjectResponseSchema(
        data=ProjectSchema.from_orm(project_state),
        message="Project updated",
        success=True
    )


async def delete(_id: uuid.UUID):
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

        logging.warning(project)
        _project = ProjectSchema.from_orm(project)

        await upload_images(_project, [])

        session.delete(project)
        session.commit()

        return ProjectResponseSchema(data=project, message="Project deleted", success=True)
