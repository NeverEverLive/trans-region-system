from pydantic import BaseModel


class FilterSchema(BaseModel):
    """Схема фильтров"""
    text: str | None
    sort: bool | None
