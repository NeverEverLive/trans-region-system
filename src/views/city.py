import uuid

from fastapi import APIRouter, Response

from src.schemas.city import CityResponseSchema, CitySchema, CitiesResponseSchema
from src.pipelines.city import create, update, get_all, get, delete


router = APIRouter()


@router.post(
    "",
    response_model=CityResponseSchema,
    status_code=201,
)
def create_city_endpoint(city: CitySchema, response: Response):
    return create(city)


@router.get(
    "",
    response_model=CitiesResponseSchema,
    status_code=200
)
def get_cities_endpoint():
    return get_all()


@router.get(
    "{_id}",
    response_model=CityResponseSchema,
    status_code=200
)
def get_city_endpoint(_id: uuid.UUID):
    return get(_id)


@router.put(
    "", 
    response_model=CityResponseSchema,
    status_code=200
)
async def update_city_endpoint(city: CitySchema):
    return update(city)


@router.delete(
    "{_id}",
    response_model=CityResponseSchema,
    status_code=202
)
async def delete_city_endpoint(_id: uuid.UUID):
    return delete(_id)
