from pydantic_settings import BaseSettings, SettingsConfigDict


class WebConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='WEB_')

    port: int
    debug: bool
    url: str


WEB_CONFIG = WebConfig()
