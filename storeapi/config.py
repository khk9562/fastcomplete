from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    class Config:
        env_file: str = ".env"


class GlobalConfig(BaseConfig):
    DATABSE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(BaseConfig):
    class Config:
        # .env file we're going to prefix all the variables which are these two for now with dev underscore and then that's going to populate those environment variables if we use dev config.
        env_prefix = "DEV_"


class ProdConfig(BaseConfig):
    class Config:
        env_prefix = "PROD_"


class TestConfig(BaseConfig):
    DATABSE_URL: Optional[str] = "sqlite:///./test.db"
    DB_FORCE_ROLL_BACK: bool = True

    class Config:
        env_prefix = "TEST_"


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
