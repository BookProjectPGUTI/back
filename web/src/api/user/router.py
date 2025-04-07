from uuid import UUID

from fastapi import APIRouter, status, Body, Path, Query

from src.api.user.dto import UserResponse, UserNameDTO, UserAddressCreateDTO, UserAddressResponse
from src.database.postgres.depends import get_session_depends
from src.domain.auth.depends import user_depends
from src.domain.auth.exception import INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES
from src.domain.exchange.service import validate_user_can_edit_setup
from src.domain.maker.exception import MAKER_ALREADY_EXISTS
from src.domain.taker.exception import TAKER_ALREADY_EXISTS
from src.domain.user.exception import USER_NOT_FOUND, USER_UNCONFIRMED, USER_DISABLED
from src.domain.user.service import get_users_me, update_user, get_user_by_id
from src.domain.user_address.dto import UserAddressDTO
from src.domain.user_address.exception import USER_ADDRESS_NOT_FOUND
from src.domain.user_address.service import create_user_address, get_user_addresses, update_user_address
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


@users_router_v1.get(
    path='',
    status_code=status.HTTP_200_OK,
    summary='Пользователь',
    description=build_description(
        'Возвращает информацию о пользователе.',
        {184}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
    ),
    response_model=UserResponse,
)
async def get_users_by_id_endpoint(
        user: user_depends,
        session: get_session_depends,
        user_id: UUID = Query(...)
) -> UserResponse:
    return await get_user_by_id(session, user_id)


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
        MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS
    ),
)
async def update_user_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: UserNameDTO = Body(...),
):
    await validate_user_can_edit_setup(session, user)
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
        MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS
    ),
    response_model=UserAddressDTO,
)
async def create_user_address_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: UserAddressCreateDTO = Body(...),
) -> UserAddressDTO:
    await validate_user_can_edit_setup(session, user)
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


@users_router_v1.put(
    path='/addresses/{user_address_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Обновить адрес',
    description=build_description(
        'Обновить информации об адресе.',
        {150}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        USER_ADDRESS_NOT_FOUND, MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS
    ),
)
async def update_user_address_endpoint(
        user: user_depends,
        session: get_session_depends,
        user_address_id: UUID = Path(...),
        body: UserAddressCreateDTO = Body(...),
):
    await validate_user_can_edit_setup(session, user)
    await update_user_address(session, user, user_address_id, body)
