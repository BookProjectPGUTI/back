from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exchange.dto import MakerCreateResponse, MakerResponse, ExchangeResponse
from src.domain.auth.dto import AccessTokenDTO
from src.domain.book.dal import BookDAL
from src.domain.book.exception import BOOK_NOT_FOUND
from src.domain.exchange.exception import EXCHANGE_NOT_FOUND
from src.domain.maker.dal import MakerDAL
from src.domain.maker.exception import MAKER_NOT_FOUND
from src.domain.maker.model import Maker


async def create_maker(
        user: AccessTokenDTO,
        session: AsyncSession
) -> MakerCreateResponse:
    maker_dal = MakerDAL(session)
    book_dal = BookDAL(session)

    book = await book_dal.get_current_book(user.sub)
    if book is None:
        raise BOOK_NOT_FOUND

    maker: Maker = await maker_dal.insert(  # type: ignore
        {
            Maker.user_id: user.sub,
            Maker.book_id: book.id,
        },
        return_value=True
    )
    if maker is None:
        raise MAKER_NOT_FOUND

    return MakerCreateResponse(
        id=maker.id,
        book=book,
    )


async def get_makers(
        user: AccessTokenDTO,
        session: AsyncSession
) -> MakerResponse:
    maker_dal = MakerDAL(session)

    makers = await maker_dal.get_matched_makers(user.sub)

    return MakerResponse(
        makers=makers
    )


async def get_current_exchange(
        user: AccessTokenDTO,
        session: AsyncSession
) -> ExchangeResponse:
    maker_dal = MakerDAL(session)

    exchange = await maker_dal.get_current_maker(user.sub)
    if exchange is None:
        raise EXCHANGE_NOT_FOUND
    return exchange
