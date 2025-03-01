from fastapi import APIRouter, status, Body

from src.api.wish_list.dto import WishListCreateDTO, WishListResponse
from src.database.postgres.depends import get_session_depends
from src.domain.auth.depends import user_depends
from src.domain.auth.exception import INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES
from src.domain.genre.exception import GENRE_NOT_FOUND
from src.domain.user.exception import USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED
from src.domain.wish_list.service import create_wish_list
from src.utils.router_utils import build_description, build_exception_responses

wish_list_router_v1 = APIRouter(
    prefix='/wish-list',
    tags=['Wish List']
)


@wish_list_router_v1.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    summary='Желаемые жанры',
    description=build_description(
        'Создание списка желаемых жанров.',
        {133}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        GENRE_NOT_FOUND,
    ),
    response_model=WishListResponse,
)
async def create_wish_list_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: WishListCreateDTO = Body(...),
) -> WishListResponse:
    return await create_wish_list(session, user, body)
