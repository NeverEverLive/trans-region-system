from fastapi import APIRouter

from src.schemas.user import UserResponseSchema, UserSchema
from src.pipelines.user import create_user

router = APIRouter(prefix="/user")


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=201,
)
def register_user(user: UserSchema):
    return create_user(user)
