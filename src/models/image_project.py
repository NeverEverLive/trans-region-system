import datetime

from sqlalchemy import Column, func, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from sqlalchemy.types import String
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import BaseModel


class ImageProject(BaseModel):
    # table name
    __tablename__ = "image_project"

    id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    path = Column(String, nullable=False)

    inserted_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=datetime.datetime.now, nullable=False
    )

    project = relationship("Project", back_populates="images", uselist=False)

    __table_args__ = (
        PrimaryKeyConstraint(id),
        ForeignKeyConstraint(
            (project_id,),
            ("project.id",),
        )
    )
