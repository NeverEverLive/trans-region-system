import logging
import uuid
from pathlib import Path

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select,  or_, func
from pydantic import parse_obj_as

from src.exceptions.project import ProjectException, ProjectDeleteException
from src.models.base import get_session
from src.models.project import Project
from src.schemas.filter import FilterSchema
from src.schemas.project import ProjectSchema, ProjectResponseSchema, ProjectsResponseSchema, ProjectResSchema
from src.settings import image_settings


async def create(project: ProjectSchema, preview: UploadFile):
    preview_path = None
    if preview:
        await upload_preview(preview)
        preview_path = image_settings.get_url(preview.filename)

    project_state = Project().fill(**project.dict(), preview=preview_path)

    with get_session() as session:
        session.add(project_state)
        session.commit()
        project = ProjectResSchema.from_orm(project)
        project.preview = preview_path
        return ProjectResponseSchema(
            data=project,
            message="Project created", 
            success=True
        )


def get_all(filters: FilterSchema):
    query = select(
        Project.id,
        Project.name,
        Project.preview,
        Project.price,
        Project.city_name,
    )

    if filters:
        if filters.text:
            query = query.where(
                or_(
                    func.lower(Project.name).ilike(f"{filters.text.lower()}%"),
                    func.lower(Project.city_name).ilike(f"{filters.text.lower()}%"),
                )
            )

        if filters.sort:
            query = query.order_by(
                Project.inserted_at.desc()
            )
        else:
            query = query.order_by(
                Project.inserted_at.asc()
            )

    with get_session() as session:
        return ProjectsResponseSchema(
            data=parse_obj_as(list[ProjectSchema], session.execute(query).fetchall()),
            message="Project accessed",
            success=True
        ).dict()


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

    return ProjectResponseSchema(
        data={**ProjectSchema.from_orm(project).dict()},
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
    with open(image_settings.get_file_location(preview.filename), "wb") as image:
        image.write(await preview.read())


async def update(project: ProjectSchema, preview: UploadFile):
    preview_path = None

    if preview:
        await upload_preview(preview)
        preview_path = image_settings.get_url(preview.filename)

    project_state = Project().fill(**project.dict(), preview=preview_path)

    with get_session() as session:
        session.merge(project_state)
        session.commit()
        project = ProjectResSchema.from_orm(project)
        project.preview = preview_path
        return ProjectResponseSchema(
            data=project,
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

        session.delete(project)
        session.commit()

        return ProjectResponseSchema(data=project, message="Project deleted", success=True)
