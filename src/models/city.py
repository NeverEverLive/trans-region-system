import datetime

from sqlalchemy import Column, func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from sqlalchemy.types import String
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class City(BaseModel):
    # table name
    __tablename__ = "city"

    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name = Column(String, nullable=False)

    inserted_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=datetime.datetime.now, nullable=False
    )

    project = relationship("Project", back_populates="city", uselist=True)

    __table_args__ = (PrimaryKeyConstraint(id),)
