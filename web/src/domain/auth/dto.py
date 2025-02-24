import uuid
from typing import Self
from uuid import UUID

from pydantic import Field

from src.domain.abc.dto import ABCDTO
from src.utils.time_utils import get_now


class AccessTokenDTO(ABCDTO):
    jti: UUID = Field(..., default_factory=uuid.uuid4, description='ID токена')
    sub: UUID = Field(..., description='ID пользователя')
    exp: int = Field(..., description='Дата последней активности в TIMESTAMP')

    @classmethod
    def factory(cls, user_id: UUID, exp: int) -> Self:
        return cls(
            sub=user_id,
            exp=int(get_now(seconds=exp).timestamp()),
        )


class RefreshTokenDTO(ABCDTO):
    jti: UUID = Field(..., default_factory=uuid.uuid4, description='ID токена')
    sub: UUID = Field(..., description='ID пользователя')
    exp: int = Field(..., description='Дата последней активности в TIMESTAMP')

    @classmethod
    def factory(cls, user_id: UUID, exp: int):
        return cls(
            sub=user_id,
            exp=int(get_now(seconds=exp).timestamp()),
        )
