import uuid

from sqlalchemy import select
from pydantic import parse_obj_as

from src.exceptions.city import CityException, CityDeleteException
from src.models.base import get_session
from src.models.city import City
from src.schemas.city import CitySchema, CityResponseSchema, CitiesResponseSchema

def create(city: CitySchema):
    city_state = City().fill(**city.dict())

    with get_session() as session:
        session.add(city_state)
        session.commit()

        return CityResponseSchema(data=CitySchema.from_orm(city_state), message="City created", success=True)


def get_all():
    return CitiesResponseSchema(
        data=parse_obj_as(list[CitySchema], City.all()),
        message="Cities accessed",
        success=True
    )


def get(_id: uuid.UUID):
    query = select(
        City
    ).where(
        City.id == _id
    ).limit(1)

    with get_session() as session:
        city = session.execute(query).scalar()
    
    if not city:
        raise CityException(
            status_code=400,
            message="City not found"
        )

    return CityResponseSchema(
        data=city,
        message="City accessed",
        success=True
    )


def update(city: CitySchema):
    city_state = City().fill(**city.dict())

    with get_session() as session:
        session.merge(city_state)
        session.commit()

    return CityResponseSchema(
        data=CitySchema.from_orm(city_state),
        message="City updated",
        success=True
    )


def delete(_id: uuid.UUID):
    query = select(
        City
    ).where(
        City.id == _id
    ).limit(1)

    with get_session() as session:
        city = session.execute(query).scalar()

        if not city:
            raise CityDeleteException(
                status_code=404,
                message="City not found"
            )

        session.delete(city)
        session.commit()

        return CityResponseSchema(data=city, message="City deleted", success=True)
