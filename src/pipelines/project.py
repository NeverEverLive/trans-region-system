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
    """
        Описание:
            Создать проект
        Входные параметры:
            :project: ProjectSchema - данные проекта
            :preview: UploadFile - превью для проекта
        Возвращаемые параметры:
            Созданный проект типа ProjectResponseSchema
    """
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
    """
        Описание:
            Получить все проекты
        Входные параметры:
            :filters: FilterSchema - Фильтры применяемы к списку
        Возвращаемые параметры:
            Список проектов типа ProjectsResponseSchema
    """
    query = select(
        Project.id,
        Project.name,
        Project.preview,
        Project.price,
        Project.city_name,
    )

    if filters:
        # Фильтрация по тексту
        if filters.text:
            query = query.where(
                or_(
                    func.lower(Project.name).ilike(f"{filters.text.lower()}%"),
                    func.lower(Project.city_name).ilike(f"{filters.text.lower()}%"),
                )
            )
        # Сортировка проектов по дате
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
    """
        Описание:
            Получить один проект
        Входные параметры:
            :_id: uuid.UUID - id получаемого проекта
        Возвращаемые параметры:
            Объект проекта типа ProjectResponseSchema
    """
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
        data={**ProjectResSchema.from_orm(project).dict()},
        message="Project accessed",
        success=True
    )


def get_image(path: str):
    """
        Описание:
            Получить изображение
        Входные параметры:
            :path: str - путь до картинки
        Возвращаемые параметры:
            Изображение типа FileResponse
    """
    response = FileResponse(
        path=Path(path.replace("%", "/")),
        media_type="image/webp",
        filename=path.split("/")[-1],
    )
    response.direct_passthrough = False
    return response


async def upload_preview(preview: UploadFile):
    """
        Описание:
            Загрузить превью
        Входные параметры:
            :preview: UploadFile - загружаемое превью
        Возвращаемые параметры:
            None
    """
    with open(image_settings.get_file_location(preview.filename), "wb") as image:
        image.write(await preview.read())


async def update(project: ProjectSchema, preview: UploadFile):
    """
        Описание:
            Обновить проект
        Входные параметры:
            :project: ProjectSchema - данные проекта
            :preview: UploadFile - превью для проекта
        Возвращаемые параметры:
            Обновленный проект типа ProjectResponseSchema
    """
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
    """
        Описание:
            Удалить проект
        Входные параметры:
            :_id: uuid.UUID - id удаляемого проекта
        Возвращаемые параметры:
            Удаленный проекта типа ProjectResponseSchema
    """
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
