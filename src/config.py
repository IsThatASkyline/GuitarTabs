import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str

    class Config:
        if os.getenv("PROD"):
            env_file = ".env"
        elif os.getenv("TEST"):
            env_file = ".test.env"
        else:
            env_file = ".dev.env"


def get_settings() -> Settings:
    return Settings()
