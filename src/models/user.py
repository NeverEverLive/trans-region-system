import logging
from sqlalchemy import Column, func, event, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String, LargeBinary, DateTime
from sqlalchemy.schema import DDL

from src.models.base import BaseModel
from src.schemas.user import UserSchema


class UserModel(BaseModel):
    """Таблица пользователя"""
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    email = Column(String, unique=True, nullable=False)
    hash_password = Column(LargeBinary, nullable=False)
    created_on = Column(DateTime, nullable=False, server_default=func.now())


    __table_args__ = (PrimaryKeyConstraint(id),)

# Скрипт создания админа если его нет, при запуске проекта
def create_admin():
    """DDL при создании таблицы добавляет пользователя admin"""
    admin_user = {
        "email": "admin@admin.com",
        "password": "password",
    }

    serializing_data = UserSchema.parse_obj(admin_user)
    return DDL(
        f"""INSERT INTO public.user(id, email, hash_password)
                VALUES
                ('{serializing_data.id}', '{serializing_data.email}', '{str(serializing_data.hash_password)[2:-1]}')
                ON CONFLICT DO NOTHING"""
    )

event.listen(UserModel.__table__, "after_create", create_admin())
