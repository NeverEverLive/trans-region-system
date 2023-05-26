import datetime

from sqlalchemy import Column, func, PrimaryKeyConstraint
from sqlalchemy.types import DateTime
from sqlalchemy.types import String
from sqlalchemy.types import BigInteger
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class Project(BaseModel):
    # table name
    __tablename__ = "project"

    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    city_name = Column(String, nullable=False)

    inserted_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=datetime.datetime.now, nullable=False
    )

    __table_args__ = (PrimaryKeyConstraint(id),)
