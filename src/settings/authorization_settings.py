from pydantic import BaseSettings
from pydantic import Field


class TokenAuthorization(BaseSettings):
    token_ttl: int = Field(env="TOKEN_TTL", default=30)
    algorithms: str = Field(env="ALGORITHMS", default="HS256")
    secret_key: str = Field(env="SECRET_KEY", default="bad_key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
