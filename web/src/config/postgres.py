from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    user: str
    password: str
    host: str
    port: int
    db: str
    driver: str = 'postgresql+asyncpg'

    def connection_url(self) -> URL:
        return URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def connection_url_str(self) -> str:
        return f'{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


try:
    POSTGRES_CONFIG = PostgresConfig(_env_file='.env', _env_prefix='POSTGRES_')  # type: ignore
except ValidationError:
    ALEMBIC_POSTGRES_CONFIG = PostgresConfig(_env_file='.migration.env', _env_prefix='POSTGRES_')  # type: ignore
