from fastapi import APIRouter, status, Body

from src.api.book.dto import BookCreateDTO, BookResponse
from src.database.postgres.depends import get_session_depends
from src.domain.auth.depends import user_depends
from src.domain.auth.exception import INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES
from src.domain.author.exception import AUTHOR_NOT_FOUND
from src.domain.book.exception import BOOK_NOT_FOUND, BOOK_ALREADY_EXISTS
from src.domain.book.service import create_book, get_book, update_book
from src.domain.exchange.service import validate_user_can_edit_setup
from src.domain.genre.exception import GENRE_NOT_FOUND
from src.domain.maker.exception import MAKER_ALREADY_EXISTS
from src.domain.taker.exception import TAKER_ALREADY_EXISTS
from src.domain.user.exception import USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED
from src.utils.router_utils import build_description, build_exception_responses

books_router_v1 = APIRouter(
    prefix='/books',
    tags=['Books']
)


@books_router_v1.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    summary='Создать книгу',
    description=build_description(
        'Создать книгу и автора. А также привязать жанры к книге.',
        {116}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        GENRE_NOT_FOUND, MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS
    ),
    response_model=BookResponse,
)
async def create_books_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: BookCreateDTO = Body(...)
) -> BookResponse:
    await validate_user_can_edit_setup(session, user)
    return await create_book(session, user, body)


@books_router_v1.get(
    path='',
    status_code=status.HTTP_200_OK,
    summary='Активная книга',
    description=build_description(
        'Получить активную книгу для обмена.',
        {123}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        BOOK_NOT_FOUND, BOOK_ALREADY_EXISTS
    ),
    response_model=BookResponse,
)
async def get_books_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> BookResponse:
    return await get_book(session, user)


@books_router_v1.put(
    path='',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Обновление книги',
    description=build_description(
        'Обновить данные о текущей книге.',
        {120}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        BOOK_NOT_FOUND, MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS, AUTHOR_NOT_FOUND
    ),
)
async def update_books_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: BookCreateDTO = Body(...),
):
    await validate_user_can_edit_setup(session, user)
    return await update_book(session, user, body)
