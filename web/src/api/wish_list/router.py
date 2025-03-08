from fastapi import APIRouter, status, Body

from src.api.wish_list.dto import WishListCreateDTO, WishListResponse
from src.database.postgres.depends import get_session_depends
from src.domain.auth.depends import user_depends
from src.domain.auth.exception import INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES
from src.domain.exchange.service import validate_user_can_edit_setup
from src.domain.genre.exception import GENRE_NOT_FOUND
from src.domain.maker.exception import MAKER_ALREADY_EXISTS
from src.domain.taker.exception import TAKER_ALREADY_EXISTS
from src.domain.user.exception import USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED
from src.domain.wish_list.exception import WISH_LIST_NOT_FOUND
from src.domain.wish_list.service import create_wish_list, get_wish_list
from src.utils.router_utils import build_description, build_exception_responses

wish_list_router_v1 = APIRouter(
    prefix='/wish-list',
    tags=['Wish List']
)


@wish_list_router_v1.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    summary='Создать желаемые жанры',
    description=build_description(
        'Создание списка желаемых жанров.',
        {133}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        GENRE_NOT_FOUND, MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS
    ),
    response_model=WishListResponse,
)
async def create_wish_list_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: WishListCreateDTO = Body(...),
) -> WishListResponse:
    await validate_user_can_edit_setup(session, user)
    return await create_wish_list(session, user, body)


@wish_list_router_v1.get(
    path='',
    status_code=status.HTTP_200_OK,
    summary='Получить желаемые жанры',
    description=build_description(
        'Списка желаемых жанров.',
        {135}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        WISH_LIST_NOT_FOUND
    ),
    response_model=WishListResponse,
)
async def get_wish_list_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> WishListResponse:
    return await get_wish_list(session, user)
