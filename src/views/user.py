import uuid

from fastapi import APIRouter, Response

from src.schemas.user import UserResponseSchema, UserSchema, UsersResponseSchema, UserLoginSchema
from src.pipelines.user import sign_in, sign_up, get_users, get_user, update_user, delete_user


router = APIRouter()


@router.post(
    "/sign_in",
    response_model=UserResponseSchema,
    status_code=201,
)
def sign_in_user_endpoint(user: UserLoginSchema, response: Response):
    """Эндпоинт для авторизации пользователя"""
    user, token = sign_in(user)
    response.headers["Authorization"] = token
    response.headers["Access-Control-Expose-Headers"] = "*"
    return user


@router.post(
    "/sign_up",
    response_model=UserResponseSchema,
    status_code=201,
)
def sign_up_user_endpoint(user: UserSchema, response: Response):
    """Эндпоинт для регистрации пользователя"""
    user, token = sign_up(user)
    response.headers["Authorization"] = token
    response.headers["Access-Control-Expose-Headers"] = "*"
    return user


@router.get(
    "",
    response_model=UsersResponseSchema,
    status_code=200
)
def get_users_endpoint():
    """Эндпоинт для получения пользователей"""
    return get_users()


@router.get(
    "/{_id}",
    response_model=UserResponseSchema,
    status_code=200
)
def get_user_endpoint(_id: uuid.UUID):
    """Эндпоинт для получения пользователя"""
    return get_user(_id)


@router.put(
    "", 
    response_model=UserResponseSchema,
    status_code=200
)
async def update_user_endpoint(user: UserSchema):
    """Эндпоинт для обновления пользователя"""
    return update_user(user)


@router.delete(
    "/{_id}",
    response_model=UserResponseSchema,
    status_code=202
)
async def delete_user_endpoint(_id: uuid.UUID):
    """Эндпоинт для удаления пользователя"""
    return delete_user(_id)
