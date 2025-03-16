from uuid import UUID

from jwt import PyJWT, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.config.auth import AUTH_CONFIG
from src.domain.auth.dto import AccessTokenDTO, RefreshTokenDTO
from src.domain.auth.exception import INVALID_CREDENTIALS
from src.domain.token.dal import TokenDAL
from src.domain.token.model import Token


class JWT:
    jwt = PyJWT(
        {
            'verify_signature': True, 'verify_aud': False, 'verify_iat': False, 'verify_exp': True, 'verify_nbf': False,
            'verify_iss': False, 'verify_sub': True, 'verify_jti': True, 'verify_at_hash': False, 'require_aud': False,
            'require_iat': False, 'require_exp': True, 'require_nbf': False, 'require_iss': False, 'require_sub': True,
            'require_jti': True, 'require_at_hash': False, 'leeway': 99999,
        }
    )

    @classmethod
    def encode(cls, claims: dict[str, str | int]) -> str:
        return cls.jwt.encode(claims, AUTH_CONFIG.secret, algorithm=AUTH_CONFIG.algorithm)

    @classmethod
    def decode(cls, token: str) -> dict[str, str | int]:
        try:
            return cls.jwt.decode(token, AUTH_CONFIG.secret, algorithms=[AUTH_CONFIG.algorithm])
        except InvalidTokenError:
            raise INVALID_CREDENTIALS


async def create_tokens(
        session: AsyncSession,
        response: Response,
        user_id: UUID
) -> AccessTokenDTO:
    refresh_payload = RefreshTokenDTO.factory(user_id, AUTH_CONFIG.refresh_exp_sec)
    refresh_token = JWT.encode(claims=refresh_payload.model_dump(mode='json'))
    response.set_cookie(
        AUTH_CONFIG.refresh_key,
        refresh_token,
        AUTH_CONFIG.refresh_exp_sec,
        **AUTH_CONFIG.cookies_kwargs()
    )

    access_payload = AccessTokenDTO.factory(user_id, AUTH_CONFIG.access_exp_sec)
    access_token = JWT.encode(claims=access_payload.model_dump(mode='json'))
    response.set_cookie(
        AUTH_CONFIG.access_key,
        access_token,
        AUTH_CONFIG.access_exp_sec,
        **AUTH_CONFIG.cookies_kwargs()
    )

    token_data = [
        {
            Token.user_id: user_id,
            Token.refresh_id: refresh_payload.jti,
            Token.access_id: access_payload.jti,
        }
    ]

    token = await TokenDAL(session).get_by_filter({Token.user_id: user_id})
    if token is None:
        await TokenDAL(session).insert_many(token_data)
    else:
        await TokenDAL(session).update(token_data)

    return access_payload
