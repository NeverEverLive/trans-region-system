from pydantic import BaseModel


class FilterSchema(BaseModel):
    text: str | None
    sort: bool | None
