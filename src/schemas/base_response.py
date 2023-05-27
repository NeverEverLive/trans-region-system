from pydantic import BaseModel
import stringcase


class BaseResponse(BaseModel):
    """Стандартный ответ"""
    class Config:
        allow_population_by_field_name = True
        alias_generator = stringcase.camelcase

    message: str
    success: bool
