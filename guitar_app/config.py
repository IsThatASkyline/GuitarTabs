import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    DB_URL: str = os.environ.get('DB_URL')
    BOT_TOKEN: str = os.environ.get('BOT_TOKEN')

    TEST_DB_URL: str = os.environ.get('TEST_DB_URL')


def get_settings() -> Settings:
    return Settings()
