import uuid

import stringcase
from pydantic import BaseModel, Field


class ImageProjectSchema(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = stringcase.camelcase
        orm_mode = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    project_id: uuid.UUID
    path: str
