import logging
import os
from pathlib import Path

from environs import Env

logger = logging.getLogger("uvicorn")


BASE_DIR = Path(__file__).resolve().parent
STATIC_PATH = Path("pages/static")
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_PATH)

TEMPLATE_PATH = Path("pages/templates")
TEMPLATE_ROOT = os.path.join(BASE_DIR, TEMPLATE_PATH)

env = Env()
env.read_env()


class AuthConfig:
    secret_key = env.str("SECRET_KEY")
    access_token_expire_minutes = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")


class DBConfig:
    MONGO_URI: str
    MONGO_DB: str


class DevDBConfig(DBConfig):
    MONGO_URI = env.str("MONGO_URI")
    MONGO_DB = env.str("MONGO_DB")


class TestDBConfig(DBConfig):
    MONGO_URI = env.str("MONGO_TEST_URI")
    MONGO_DB = env.str("MONGO_TEST_DB")


def get_db_config():
    environment = env.str("ENV", "dev").lower()
    if environment == "test":
        return TestDBConfig
    return DevDBConfig
