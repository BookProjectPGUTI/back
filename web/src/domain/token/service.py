from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.config.auth import AUTH_CONFIG
from src.domain.auth.dto import AccessTokenDTO, RefreshTokenDTO
from src.domain.auth.service import JWT
from src.domain.token.dal import TokenDAL
from src.domain.token.model import Token


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
            Token.user_id.key: user_id,
            Token.refresh_id.key: refresh_payload.jti,
            Token.access_id.key: access_payload.jti,
        }
    ]

    token = await TokenDAL(session).get_by_user_id(user_id)
    if token is None:
        await TokenDAL(session).insert(token_data)
    else:
        await TokenDAL(session).update(token_data)

    return access_payload
