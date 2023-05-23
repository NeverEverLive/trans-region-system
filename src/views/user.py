import uuid

from fastapi import APIRouter, Response

from src.schemas.user import UserResponseSchema, UserSchema, UsersResponseSchema
from src.pipelines.user import sign_user, get_users, get_user, update_user, delete_user


router = APIRouter()


@router.post(
    "",
    response_model=UserResponseSchema,
    status_code=201,
)
def sign_user_endpoint(user: UserSchema, response: Response):
    user, token = sign_user(user)
    response.headers["Authorization"] = token
    response.headers["Access-Control-Expose-Headers"] = "*"
    return user


@router.get(
    "",
    response_model=UsersResponseSchema,
    status_code=200
)
def get_users_endpoint():
    return get_users()


@router.get(
    "{_id}",
    response_model=UserResponseSchema,
    status_code=200
)
def get_user_endpoint(_id: uuid.UUID):
    return get_user(_id)


@router.put(
    "", 
    response_model=UserResponseSchema,
    status_code=200
)
async def update_user_endpoint(user: UserSchema):
    return update_user(user)


@router.delete(
    "{_id}",
    response_model=UserResponseSchema,
    status_code=202
)
async def delete_user_endpoint(_id: uuid.UUID):
    return delete_user(_id)
