from fastapi import APIRouter, status

from src.api.exchange.dto import MakerCreateResponse
from src.database.postgres.depends import get_session_depends
from src.domain.auth.depends import user_depends
from src.domain.auth.exception import INVALID_CREDENTIALS, REFRESH_NOT_FOUND, REFRESH_EXPIRES
from src.domain.book.exception import BOOK_NOT_FOUND
from src.domain.maker.exception import MAKER_ALREADY_EXISTS
from src.domain.maker.service import create_maker
from src.domain.taker.exception import TAKER_ALREADY_EXISTS
from src.domain.user.exception import USER_NOT_FOUND, USER_DISABLED, USER_UNCONFIRMED, USER_NOT_NAMED
from src.domain.user_address.exception import USER_ADDRESS_NOT_FOUND
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
        MAKER_ALREADY_EXISTS, TAKER_ALREADY_EXISTS, BOOK_NOT_FOUND, USER_NOT_NAMED, USER_ADDRESS_NOT_FOUND
    ),
    response_model=MakerCreateResponse,
)
async def create_maker_endpoint(
        user: user_depends,
        session: get_session_depends,
) -> MakerCreateResponse:
    return await create_maker(user, session)
