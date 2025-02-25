from typing import Annotated

from fastapi import Response, HTTPException, Security
from fastapi.security import APIKeyCookie, HTTPBearer, HTTPAuthorizationCredentials

from src.config.auth import AUTH_CONFIG
from src.database.postgres.depends import get_session_depends
from src.domain.auth.dto import AccessTokenDTO, RefreshTokenDTO
from src.domain.auth.exception import (
    ACCESS_NOT_FOUND, ACCESS_EXPIRES, REFRESH_NOT_FOUND, REFRESH_EXPIRES
)
from src.domain.token.dal import TokenDAL
from src.domain.token.model import Token
from src.domain.token.service import create_tokens, JWT
from src.domain.user.dal import UserDAL
from src.domain.user.exception import USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED
from src.utils.time_utils import get_now


refresh_bearer_depends = Annotated[
    HTTPAuthorizationCredentials | None,
    Security(
        HTTPBearer(
            scheme_name='Bearer', description='Set refresh token to header (without Bearer in start).',
            auto_error=False
        )
    )
]

refresh_cookies_depends = Annotated[
    str | None,
    Security(
        APIKeyCookie(
            name=AUTH_CONFIG.refresh_key, description='Set refresh token to cookies.', auto_error=False,
        )
    )
]

access_bearer_depends = Annotated[
    HTTPAuthorizationCredentials | None,
    Security(
        HTTPBearer(
            scheme_name='Bearer', description='Set refresh token to header (without Bearer in start).',
            auto_error=False
        )
    )
]

access_cookies_depends = Annotated[
    str | None,
    Security(
        APIKeyCookie(
            name=AUTH_CONFIG.access_key, description='Set refresh token to cookies.', auto_error=False,
        )
    )
]


class UserFilter:
    def __init__(self, is_make_refresh: bool = False):
        self.is_make_refresh = is_make_refresh

    async def __call__(
            self,
            response: Response,
            session: get_session_depends,
            access_bearer_token: access_bearer_depends,
            access_cookies_token: access_cookies_depends,
            refresh_bearer_token: refresh_bearer_depends,
            refresh_cookies_token: refresh_cookies_depends,
    ) -> AccessTokenDTO:
        self.session = session
        self.access_bearer_token = access_bearer_token
        self.access_cookies_token = access_cookies_token
        self.refresh_bearer_token = refresh_bearer_token
        self.refresh_cookies_token = refresh_cookies_token

        try:
            access_payload = await self.check_access()
            if self.is_make_refresh is True:
                token_db = await self.check_refresh()
                await create_tokens(session, response, token_db.user_id)
            return access_payload
        except HTTPException as e:
            if e in (ACCESS_EXPIRES, ACCESS_NOT_FOUND):
                token_db = await self.check_refresh()
                access_payload = await create_tokens(session, response, token_db.user_id)
                return access_payload
            else:
                raise e

    async def check_access(self) -> AccessTokenDTO:
        if self.access_bearer_token is not None:
            token = self.access_bearer_token.credentials
        elif self.access_cookies_token is not None:
            token = self.access_cookies_token
        else:
            raise ACCESS_NOT_FOUND

        payload = AccessTokenDTO.model_validate(JWT.decode(token))

        if payload.exp < int(get_now().timestamp()):
            raise ACCESS_EXPIRES

        if payload.exp > int(get_now(hours=1).timestamp()):
            self.is_make_refresh = True

        token_db = await TokenDAL(self.session).get_by_user_id(payload.sub)
        if token_db is None:
            raise ACCESS_NOT_FOUND

        if token_db.access_id != payload.jti:
            raise ACCESS_EXPIRES

        user = await UserDAL(self.session).get_by_id(payload.sub)
        if user is None:
            raise USER_NOT_FOUND

        if user.is_enabled is False:
            raise USER_DISABLED

        if user.is_confirmed is False:
            raise USER_UNCONFIRMED

        return payload

    async def check_refresh(
            self
    ) -> Token:
        if self.refresh_bearer_token is not None:
            token = self.refresh_bearer_token.credentials
        elif self.refresh_cookies_token is not None:
            token = self.refresh_cookies_token
        else:
            raise REFRESH_NOT_FOUND

        payload = RefreshTokenDTO.model_validate(JWT.decode(token))
        if payload.exp < int(get_now().timestamp()):
            raise REFRESH_EXPIRES

        if payload.exp > int(get_now(days=2).timestamp()):
            self.is_make_refresh = True

        token_db = await TokenDAL(self.session).get_by_user_id(payload.sub)
        if token_db is None:
            raise REFRESH_NOT_FOUND

        if token_db.refresh_id != payload.jti:
            raise REFRESH_EXPIRES

        user = await UserDAL(self.session).get_by_id(payload.sub)
        if user is None:
            raise USER_NOT_FOUND

        if user.is_enabled is False:
            raise USER_DISABLED

        if user.is_confirmed is False:
            raise USER_UNCONFIRMED

        return token_db
