import logging
import uuid
import bcrypt

from sqlalchemy import select
from pydantic import parse_obj_as

from src.exceptions.user import UserDeleteException, UserException, UserCreateException
from src.exceptions.authentication import AuthenticationException
from src.models.base import get_session
from src.models.user import UserModel
from src.authorization.jwt_handler import encode_jwt_token
from src.schemas.user import UserSchema, UserResponseSchema, UsersResponseSchema, UserSecure, UserLoginSchema


def sign_in(user: UserLoginSchema):
    query = select(
        UserModel
    ).where(
        UserModel.email == user.email
    ).limit(1)

    with get_session() as session:
        user_state = session.execute(query).scalar()

    if not user_state:
        raise AuthenticationException(status_code=400, message="Неверная почта")

    if not bcrypt.checkpw(user.hash_password, user_state.hash_password):
        raise AuthenticationException(status_code=400, message="Неверный пароль")

    token = encode_jwt_token(user_state.id)

    if user_state:
        return UserResponseSchema(
            data=user_state,
            success=True,
            message="You're successfully signed in"
        ), token


def sign_up(user: UserSchema) -> UserResponseSchema:
    user_state = UserModel.fill(**user.dict())
    token = encode_jwt_token(user.id)

    with get_session() as session:
        session.add(user_state)
        try:
            session.commit()
        except Exception:
            raise UserCreateException(status_code=400, message="User already exist")
    
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
