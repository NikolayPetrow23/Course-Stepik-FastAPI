from pydantic import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url(self):
        user = f"{self.DB_USER}:{self.DB_PASS}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{user}@{database}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def test_database_url(self):
        user = f"{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
        database = f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        return f"postgresql+asyncpg://{user}@{database}"

    REDIS_PORT: int
    REDIS_HOST: str

    EMAIL_HOST: str
    EMAIL_HOST_USER: str
    EMAIL_PORT: int
    EMAIL_HOST_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()
