import uuid
import json

import stringcase
from pydantic import BaseModel, Field

from src.schemas.base_response import BaseResponse


class ProjectSchema(BaseModel):
    """Схема проекта"""
    class Config:
        allow_population_by_field_name = True
        alias_generator = stringcase.camelcase
        orm_mode = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    city_name: str
    name: str
    price: int
    description: str | None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ProjectResSchema(BaseModel):
    """Схема возвращаемого проекта"""
    class Config:
        allow_population_by_field_name = True
        alias_generator = stringcase.camelcase
        orm_mode = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    price: int
    description: str | None
    preview: str | None
    city_name: str | None

class ProjectResponseSchema(BaseResponse):
    """Схема ответа проекта"""
    data: ProjectResSchema


class ProjectsResponseSchema(BaseResponse):
    """Схема ответа проектов"""
    data: list[ProjectResSchema]
