import datetime

from sqlalchemy import Column, func, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from sqlalchemy.types import String
from sqlalchemy.types import BigInteger
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class Project(BaseModel):
    # table name
    __tablename__ = "project"

    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    city_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)

    inserted_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=datetime.datetime.now, nullable=False
    )

    city = relationship("City", back_populates="project", uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (city_id,),
            ("city.id",),
        )
    )
