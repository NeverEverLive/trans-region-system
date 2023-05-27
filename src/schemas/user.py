import logging
import uuid

import bcrypt
from pydantic import BaseModel, Field, EmailStr, validator

from src.schemas.base_response import BaseResponse


class UserSchema(BaseModel):
    """Схема пользователя"""
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
    """Схема пользователя для авторизации"""
    email: EmailStr
    hash_password: bytes = Field(alias="password")


class UserSecure(BaseModel):
    """Защищенная схема пользователя"""
    id: uuid.UUID
    email: EmailStr

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserResponseSchema(BaseResponse):
    """Схема ответа пользователя"""
    class Config:
        orm_mode = True

    data: UserSecure


class UsersResponseSchema(BaseResponse):
    """Схема пользователей"""
    data: list[UserSecure]
