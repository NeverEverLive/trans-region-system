import uuid

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
