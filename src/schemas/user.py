import uuid

from pydantic import BaseModel, Field

from src.schemas.base_response import BaseResponse


class UserSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str


class UserResponseSchema(BaseResponse):
    data: UserSchema
