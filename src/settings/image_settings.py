from pydantic import BaseSettings, Field


class ImageSettings(BaseSettings):
    bucket_path: str = Field(env="BUCKET_PATH", default="127.0.0.1")

    def get_url(self, file_name: str):
        return f'{self.bucket_path}/images/{file_name}'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
