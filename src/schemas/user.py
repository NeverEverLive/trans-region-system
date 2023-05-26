import logging
import uuid

import bcrypt
from pydantic import BaseModel, Field, EmailStr, validator

from src.schemas.base_response import BaseResponse


class UserSchema(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        allow_population_by_field_name = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: EmailStr
    hash_password: bytes = Field(alias="password")

    @validator("hash_password", pre=True)
    def password_hasher(cls, value: str) -> bytes:
        if isinstance(value, str):
            return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        elif isinstance(value, bytes):
            return value
        else:
            raise ValueError("Пароль должен быть передан строкой.")


class UserLoginSchema(BaseModel):
    email: EmailStr
    hash_password: bytes = Field(alias="password")


class UserSecure(BaseModel):
    id: uuid.UUID
    email: EmailStr

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserResponseSchema(BaseResponse):
    class Config:
        orm_mode = True

    data: UserSecure


class UsersResponseSchema(BaseResponse):
    data: list[UserSecure]


class UserID(BaseModel):
    id: uuid.UUID

    class Config:
        orm_mode = True
