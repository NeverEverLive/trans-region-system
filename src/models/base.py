from contextlib import contextmanager
from typing import ContextManager
from typing import List
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src.settings import postgres_settings


class BaseModel(DeclarativeBase):
    """Postgres base model"""

    _session: scoped_session[Session] | None = None

    @classmethod
    def set_session(cls, session: scoped_session[Session]) -> None:
        cls._session = session

    @classmethod
    def first(cls) -> "Type[BaseModel]":
        return cls._session.query(cls).first()

    @classmethod
    def all(cls) -> "List[Type[BaseModel]]":
        return cls._session.query(cls).all()

    @classmethod
    def fill(cls, **data) -> "BaseModel":
        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj


class BaseMaterializedViewModel(BaseModel):
    """Postgres base materialized view"""
    __abstract__ = True

    @classmethod
    def refresh(cls, concurrently=True):
        _concurrently = "CONCURRENTLY" if concurrently else ""
        with get_session(autocommit=True) as session:
            session.execute(text(f"REFRESH MATERIALIZED VIEW {_concurrently} {cls.__tablename__}"))


@contextmanager
def get_session(autocommit=False) -> ContextManager[Session]:
    """Get session"""
    engine = create_engine(postgres_settings.get_url())
    session = Session(engine)
    try:
        yield session
    finally:
        if autocommit:
            session.commit()
        session.close()


def set_session():
    """Create session"""
    engine = create_engine(postgres_settings.get_url())
    db_session = scoped_session(sessionmaker(autoflush=True, bind=engine))
    BaseModel.set_session(db_session)
    BaseModel.query = db_session.query_property()
    BaseModel.metadata.create_all(engine)
