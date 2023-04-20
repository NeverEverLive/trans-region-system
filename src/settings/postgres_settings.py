from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    host: str = Field(env="PG_HOST", default="127.0.0.1")
    port: int = Field(env="PG_PORT", default=5432)
    username: str = Field(env="PG_USERNAME", default="postgres")
    password: str = Field(env="PG_PASSWORD", default="postgres")
    database: str = Field(env="PG_DATABASE", default="article")

    def get_url(self):
        return f'postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
