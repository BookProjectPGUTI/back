from fastapi import APIRouter, status, Body

from src.api.exchange.dto import MakerCreateResponse, MakerResponse, ExchangeResponse, TakerCreateResponse
from src.domain.maker.dto import MakerAcceptDTO
from src.domain.taker.dto import TakerCreateDTO
from src.database.postgres.depends import get_session_depends
from src.domain.auth.depends import user_depends
from src.domain.auth.exception import INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES
from src.domain.book.exception import BOOK_NOT_FOUND
from src.domain.book_genre.exception import BOOK_GENRE_NOT_FOUND
from src.domain.exchange.exception import EXCHANGE_NOT_FOUND
from src.domain.exchange.service import validate_user_can_edit_setup, validate_user_complete_setup, get_current_exchange
from src.domain.maker.exception import (
    MAKER_ALREADY_EXISTS, MAKER_NOT_FOUND, MAKER_ALREADY_TAKEN, MAKER_ALREADY_RECEIVED, MAKER_ALREADY_ACCEPTED
)
from src.domain.maker.service import create_maker, get_makers, delete_maker, accept_maker
from src.domain.taker.exception import TAKER_ALREADY_EXISTS, TAKER_ALREADY_RECEIVED, TAKER_NOT_FOUND
from src.domain.taker.service import create_taker
from src.domain.user.exception import USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED, USER_NOT_NAMED
from src.domain.user_address.exception import USER_ADDRESS_NOT_FOUND
from src.domain.wish_list.exception import WISH_LIST_NOT_FOUND
from src.utils.router_utils import build_description, build_exception_responses

exchanges_router_v1 = APIRouter(
    prefix='/exchanges',
    tags=['Exchanges']
)


@exchanges_router_v1.post(
    path='/makers',
    status_code=status.HTTP_201_CREATED,
    summary='Стать мейкером',
    description=build_description(
        'Пользователь начинает ожидать второго пользователя для обмена (Тейкера).',
        {163}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS, BOOK_NOT_FOUND, USER_NOT_NAMED, USER_ADDRESS_NOT_FOUND,
        WISH_LIST_NOT_FOUND, BOOK_GENRE_NOT_FOUND, MAKER_NOT_FOUND
    ),
    response_model=MakerCreateResponse,
)
async def create_maker_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> MakerCreateResponse:
    await validate_user_can_edit_setup(session, user)
    await validate_user_complete_setup(session, user)
    return await create_maker(user, session)


@exchanges_router_v1.get(
    path='/makers',
    status_code=status.HTTP_200_OK,
    summary='Список мейкеров',
    description=build_description(
        'Происходит фильтрация по желаемым жанрам пользователя и существующим мейкерам.',
        {158}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS, BOOK_NOT_FOUND, USER_NOT_NAMED, USER_ADDRESS_NOT_FOUND,
        WISH_LIST_NOT_FOUND, BOOK_GENRE_NOT_FOUND
    ),
    response_model=MakerResponse,
)
async def get_maker_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> MakerResponse:
    await validate_user_can_edit_setup(session, user)
    await validate_user_complete_setup(session, user)
    return await get_makers(user, session)


@exchanges_router_v1.get(
    path='/current',
    status_code=status.HTTP_200_OK,
    summary='Текущий обмен',
    description=build_description(
        'Позволяет пользователю узнать, участвует ли он в активном обмене, и является ли он мейкером '
        '(создателем заявки) или тейкером (принявшим заявку). Также возвращает информацию о паре для '
        'обмена, включая данные пользователей, книги и совпадающие жанры.',
        {161}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        BOOK_NOT_FOUND, USER_NOT_NAMED, USER_ADDRESS_NOT_FOUND, WISH_LIST_NOT_FOUND, BOOK_GENRE_NOT_FOUND,
        EXCHANGE_NOT_FOUND,
    ),
    response_model=ExchangeResponse,
)
async def get_current_exchange_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> ExchangeResponse:
    await validate_user_complete_setup(session, user)
    return await get_current_exchange(user, session)


@exchanges_router_v1.post(
    path='/takers',
    status_code=status.HTTP_201_CREATED,
    summary='Принять обмен',
    description=build_description(
        'Пользователь выбирает из списка активных мейкеров нужную пару и становится тейкером.',
        {165}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        BOOK_NOT_FOUND, USER_NOT_NAMED, USER_ADDRESS_NOT_FOUND, WISH_LIST_NOT_FOUND, BOOK_GENRE_NOT_FOUND,
        MAKER_NOT_FOUND, MAKER_ALREADY_ACCEPTED, MAKER_ALREADY_RECEIVED, MAKER_ALREADY_TAKEN
    ),
    response_model=TakerCreateResponse
)
async def create_taker_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: TakerCreateDTO = Body(...),
) -> TakerCreateResponse:
    await validate_user_can_edit_setup(session, user)
    await validate_user_complete_setup(session, user)
    return await create_taker(session, user, body)


@exchanges_router_v1.delete(
    path='',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Отменить поиск',
    description=build_description(
        'Если пользователь передумал искать пару для обмена, он может отменить свою заявку, перестав быть мейкером. '
        'После этого его заявка удаляется из системы, и другие пользователи больше не видят её в списке доступных '
        'обменов.',
        {167}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        MAKER_NOT_FOUND, MAKER_ALREADY_ACCEPTED, MAKER_ALREADY_RECEIVED, TAKER_ALREADY_RECEIVED
    )
)
async def delete_maker_endpoint(
        user: user_depends,
        session: get_session_depends,
):
    await delete_maker(user, session)


@exchanges_router_v1.put(
    path='/makers/accept',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Принять или отклонить тейкера',
    description=build_description(
        'Мейкер подтверждает обмен с тейкером или отклоняет его. '
        'После подтверждения пользователи не смогут изменять данные обмена, включая адреса доставки, ФИО, информацию '
        'о книгах и жанрах.',
        {170}
    ),
    responses=build_exception_responses(
        INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES, USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED,
        MAKER_NOT_FOUND, MAKER_ALREADY_ACCEPTED, TAKER_NOT_FOUND, TAKER_ALREADY_RECEIVED,
    )
)
async def accept_maker_endpoint(
        user: user_depends,
        session: get_session_depends,
        body: MakerAcceptDTO = Body()
):
    await accept_maker(user, session, body)
