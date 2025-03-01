from fastapi import APIRouter, status

from src.api.genre.dto import GenreResponse
from src.database.postgres.depends import get_session_depends
from src.domain.auth.depends import user_depends
from src.domain.auth.exception import INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES
from src.domain.genre.service import get_genres
from src.domain.user.exception import USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED
from src.utils.router_utils import build_description, build_exception_responses

genres_router_v1 = APIRouter(
    prefix='/genres',
    tags=['Genres']
)


@genres_router_v1.get(
    path='',
    status_code=status.HTTP_200_OK,
    summary='Жанры',
    description=build_description(
        'Возвращает список жанров.',
        {117}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
    ),
    response_model=GenreResponse,
)
async def get_genres_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> GenreResponse:
    return await get_genres(session)
