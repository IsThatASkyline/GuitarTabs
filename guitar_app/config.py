import os
from dataclasses import dataclass
from enum import Enum
import logging.config
from dotenv import find_dotenv, load_dotenv
import yaml

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

@dataclass
class RedisConfig:
    url: str = "redis"
    port: int = 6379
    db: int = 1


class StorageType(Enum):
    memory = "memory"
    redis = "redis"


@dataclass
class StorageConfig:
    type_: StorageType
    redis: RedisConfig | None = None


class Settings:
    DB_URL: str = os.environ.get("DB_URL")
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN")
    TEST_DB_URL: str = os.environ.get("TEST_DB_URL")

    storage_type: str = os.environ.get("STORAGE_TYPE", default="memory")
    REDIS_URL: str = os.environ.get("REDIS_URL")
    REDIS_PORT: int = os.environ.get("REDIS_PORT")
    REDIS_DB: int = os.environ.get("REDIS_DB")


def get_settings() -> Settings:
    return Settings()


def setup_logging():
    try:
        with open("logging.yaml") as f:
            logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)
        logger.info("Logging configured successfully")
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("logging config file not found, use basic config")