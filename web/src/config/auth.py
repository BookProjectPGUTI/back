from typing import Dict, Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AUTH_')

    secret: str
    algorithm: str = 'HS256'

    refresh_key: str = 'refresh'
    refresh_exp_sec: int = 60 * 60 * 24 * 14

    access_key: str = 'access'
    access_exp_sec: int = 60 * 60 * 24 * 2

    @staticmethod
    def cookies_kwargs() -> Dict[str, Any]:
        kwargs = {
            'samesite': 'Strict',
            'secure': False,
            'httponly': True
        }
        return kwargs


AUTH_CONFIG = AuthConfig()
