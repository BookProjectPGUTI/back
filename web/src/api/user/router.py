from fastapi import APIRouter, status, Body

from src.api.user.dto import UserResponse, UserNameDTO, UserAddressCreateDTO, UserAddressResponse
from src.database.postgres.depends import get_session_depends
from src.domain.auth.depends import user_depends
from src.domain.auth.exception import INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES
from src.domain.user.exception import USER_NOT_FOUND, USER_UNCONFIRMED, USER_DISABLED
from src.domain.user.service import get_users_me, update_user
from src.domain.user_address.dto import UserAddressDTO
from src.domain.user_address.service import create_user_address, get_user_addresses
from src.utils.router_utils import build_description, build_exception_responses

users_router_v1 = APIRouter(
    prefix='/users',
    tags=['Users']
)


@users_router_v1.get(
    path='/me',
    status_code=status.HTTP_200_OK,
    summary='Текущий пользователь',
    description=build_description(
        'Возвращает информацию о текущем пользователе из JWT.',
        {109}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
    ),
    response_model=UserResponse,
)
async def get_users_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> UserResponse:
    return await get_users_me(session, user)


@users_router_v1.put(
    path='',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Внести ФИО пользователя',
    description=build_description(
        'Внести ФИО пользователя.',
        {137}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
    ),
)
async def update_user_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: UserNameDTO = Body(...),
):
    return await update_user(session, user, body)


@users_router_v1.post(
    path='/addresses',
    status_code=status.HTTP_201_CREATED,
    summary='Создание адреса',
    description=build_description(
        'Создание адреса пользователя.',
        {138}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
    ),
    response_model=UserAddressDTO,
)
async def create_user_address_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: UserAddressCreateDTO = Body(...),
) -> UserAddressDTO:
    return await create_user_address(session, user, body)


@users_router_v1.get(
    path='/addresses',
    status_code=status.HTTP_200_OK,
    summary='Список адресов',
    description=build_description(
        'Получить список адресов пользователя.',
        {152}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
    ),
    response_model=UserAddressResponse,
)
async def get_user_addresses_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> UserAddressResponse:
    return await get_user_addresses(session, user)
