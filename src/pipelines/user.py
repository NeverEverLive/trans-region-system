import uuid
import logging

from sqlalchemy import select, update, delete
from pydantic import parse_obj_as

from src.exceptions.user import UserDeleteException, UserException
from src.models.base import get_session
from src.models.user import UserModel
from src.authorization.jwt_handler import encode_jwt_token
from src.schemas.user import UserSchema, UserResponseSchema, UsersResponseSchema, UserSecure


def sign_user(user: UserSchema) -> UserResponseSchema:
    query = select(
        UserModel
    ).where(
        UserModel.id == user.id
    ).limit(1)

    with get_session() as session:
        user_state = session.execute(query).scalar()

    token = encode_jwt_token(user.id)
    if user_state:
        return UserResponseSchema(
            data=user,
            success=True,
            message="You're successfully signed in"
        ), token

    user_state = UserModel.fill(**user.dict())

    with get_session() as session:
        session.add(user_state)
        session.commit()
    
    return UserResponseSchema(
        data=user,
        success=True,
        message="You're successfully signed up"
    ), token


def get_users() -> UserResponseSchema:
    return UsersResponseSchema(
        data=parse_obj_as(list[UserSecure], UserModel.all()),
        message="User accessed",
        success=True
    )

def get_user(_id: uuid.UUID) -> UserResponseSchema:
    query = select(
        UserModel
    ).where(
        UserModel.id == _id
    ).limit(1)

    with get_session() as session:
        user = session.execute(query).scalar()

    if not user:
        raise UserException(
            status_code=400,
            message="User not found"
        )

    return UserResponseSchema(
        data=user,
        message="User accessed",
        success=True
    )


def update_user(user_data) -> UserResponseSchema:
    """
    Изменить пользователя
    Входные параметры:
    :params user: Данные пользователя

    Исходящие данные:
    Словарь с результатами обновления пользователя
    """

    user_state = UserModel().fill(**user_data.dict())

    with get_session() as session:
        session.merge(user_state)
        session.commit()

        return UserResponseSchema(data=UserSecure.from_orm(user_state), message="User updated", success=True)


def delete_user(_id) -> UserResponseSchema:
    """
    Удалить пользователя
    Входные параметры:
    :params user: Данные пользователя

    Исходящие данные:
    Словарь с результатами удаления пользователя
    """
    query = select(
        UserModel
    ).where(
        UserModel.id == _id
    ).limit(1)


    with get_session() as session:
        user = session.execute(query).scalar()

        if not user:
            raise UserDeleteException(
                status_code=404,
                message="User not found"
            )

        session.delete(user)
        session.commit()

        return UserResponseSchema(data=UserSecure.from_orm(user), message="User deleted", success=True)
