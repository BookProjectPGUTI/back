from uuid import UUID

from fastapi import APIRouter, status, Path, Response
from starlette.responses import HTMLResponse

from src.api.auth.dto import SignUpDTO, SignUpResponse, SignInDTO, SingInResponse
from src.database.postgres.depends import get_session_depends
from src.domain.token.service import create_tokens
from src.domain.user.exception import (
    EMAIL_ALREADY_EXISTS, USERNAME_ALREADY_EXISTS, USER_NOT_FOUND, USER_ALREADY_CONFIRMED, USER_DISABLED,
    USER_UNCONFIRMED
)
from src.domain.auth.exception import INVALID_CREDENTIALS
from src.domain.user.service import sign_up, email_accept, validate_credentials
from src.utils.router_utils import build_exception_responses, build_description

auth_router_v1 = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@auth_router_v1.post(
    path='/sign-up',
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация',
    description=build_description(
        'Регистрация пользователя, отправка сообщения с подтверждением почты.',
        {88}
    ),
    response_model=SignUpResponse,
    responses=build_exception_responses(
        EMAIL_ALREADY_EXISTS, USERNAME_ALREADY_EXISTS,
    )
)
async def sign_up_endpoint(
        session: get_session_depends,
        body: SignUpDTO,
) -> SignUpResponse:
    return await sign_up(session, body)


@auth_router_v1.get(
    path='/accept/{user_id}',
    status_code=status.HTTP_200_OK,
    summary='Подтверждение почты',
    description=build_description(
        'Ссылка на этот эндпоинт отправляется на почту.',
        {95}
    ),
    response_class=HTMLResponse,
    responses=build_exception_responses(
        USER_NOT_FOUND, USER_ALREADY_CONFIRMED, USER_DISABLED
    )
)
async def email_accept_endpoint(
        session: get_session_depends,
        user_id: UUID = Path(..., description='ID пользователя'),
) -> HTMLResponse:
    return await email_accept(session, user_id)


@auth_router_v1.post(
    path='/sign-in',
    status_code=status.HTTP_200_OK,
    summary='Авторизация',
    description=build_description(
        'Вход в аккаунт пользователя через логин и пароль.',
        {90}
    ),
    response_model=SingInResponse,
    responses=build_exception_responses(
        INVALID_CREDENTIALS, USER_NOT_FOUND, USER_UNCONFIRMED, USER_DISABLED
    )
)
async def sign_in_endpoint(
        session: get_session_depends,
        response: Response,
        body: SignInDTO,
) -> SingInResponse:
    user = await validate_credentials(session, body)
    await create_tokens(session, response, user.id)
    return SingInResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )
