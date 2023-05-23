import uuid
from pydantic import BaseModel, Field

from src.schemas.base_response import BaseResponse


class CitySchema(BaseModel):
    class Config:
        orm_mode = True
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str


class CityResponseSchema(BaseResponse):
    data: CitySchema


class CitiesResponseSchema(BaseResponse):
    data: list[CitySchema]
