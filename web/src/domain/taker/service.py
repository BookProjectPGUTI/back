from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exchange.dto import TakerCreateResponse
from src.domain.book.dal import BookDAL
from src.domain.book.exception import BOOK_NOT_FOUND
from src.domain.maker.dal import MakerDAL
from src.domain.maker.exception import (
    MAKER_NOT_FOUND,
    MAKER_ALREADY_ACCEPTED,
    MAKER_ALREADY_RECEIVED,
    MAKER_ALREADY_TAKEN
)
from src.domain.maker.model import Maker
from src.domain.taker.dal import TakerDAL
from src.domain.taker.dto import TakerCreateDTO
from src.domain.auth.dto import AccessTokenDTO
from src.domain.taker.model import Taker


async def create_taker(
        session: AsyncSession,
        user: AccessTokenDTO,
        body: TakerCreateDTO
) -> TakerCreateResponse:
    maker_dal = MakerDAL(session)
    taker_dal = TakerDAL(session)
    book_dal = BookDAL(session)

    taker = await taker_dal.get_by_filter({Taker.id: body.maker_id})
    if taker is not None:
        raise MAKER_ALREADY_TAKEN

    maker = await maker_dal.get_by_filter({Maker.id: body.maker_id})
    if maker is None:
        raise MAKER_NOT_FOUND
    if maker.is_accepted is True:
        raise MAKER_ALREADY_ACCEPTED
    if maker.is_received is True:
        raise MAKER_ALREADY_RECEIVED

    book = await book_dal.get_current_book(user.sub)
    if book is None:
        raise BOOK_NOT_FOUND

    await taker_dal.insert(
        {
            Taker.id: body.maker_id,
            Taker.user_id: user.sub,
            Taker.book_id: book.id,
        }
    )

    return TakerCreateResponse()
