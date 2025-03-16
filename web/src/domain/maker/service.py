from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exchange.dto import MakerCreateResponse, MakerResponse
from src.domain.auth.dto import AccessTokenDTO
from src.domain.book.dal import BookDAL
from src.domain.book.exception import BOOK_NOT_FOUND
from src.domain.maker.dal import MakerDAL
from src.domain.maker.dto import MakerAcceptDTO
from src.domain.maker.exception import MAKER_NOT_FOUND, MAKER_ALREADY_ACCEPTED, MAKER_ALREADY_RECEIVED
from src.domain.maker.model import Maker
from src.domain.taker.dal import TakerDAL
from src.domain.taker.exception import TAKER_ALREADY_RECEIVED, TAKER_NOT_FOUND
from src.domain.taker.model import Taker


async def create_maker(
        user: AccessTokenDTO,
        session: AsyncSession
) -> MakerCreateResponse:
    maker_dal = MakerDAL(session)
    book_dal = BookDAL(session)

    book = await book_dal.get_current_book(user.sub)
    if book is None:
        raise BOOK_NOT_FOUND

    maker = await maker_dal.insert(
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


async def delete_maker(
        user: AccessTokenDTO,
        session: AsyncSession,
):
    maker_dal = MakerDAL(session)
    taker_dal = TakerDAL(session)

    maker = await maker_dal.get_by_filter(
        {
            Maker.user_id: user.sub,
            Maker.is_received: False,
        }
    )
    if maker is None:
        raise MAKER_NOT_FOUND
    if maker.is_accepted is True:
        raise MAKER_ALREADY_ACCEPTED
    if maker.is_received is True:
        raise MAKER_ALREADY_RECEIVED

    taker = await taker_dal.get_by_filter({Taker.id: maker.id})
    if taker is not None:
        if taker.is_received is True:
            raise TAKER_ALREADY_RECEIVED

        await taker_dal.delete(id=taker.id)

    await maker_dal.delete(id=maker.id)


async def accept_maker(
        user: AccessTokenDTO,
        session: AsyncSession,
        body: MakerAcceptDTO,
):
    maker_dal = MakerDAL(session)
    taker_dal = TakerDAL(session)

    maker = await maker_dal.get_by_filter({Maker.user_id: user.sub, Maker.is_received: False})
    if maker is None:
        raise MAKER_NOT_FOUND
    if maker.is_accepted is True:
        raise MAKER_ALREADY_ACCEPTED
    if maker.is_received is True:
        raise MAKER_ALREADY_RECEIVED

    taker = await taker_dal.get_by_filter({Taker.id: maker.id})
    if taker is None:
        raise TAKER_NOT_FOUND
    if taker.is_received is True:
        raise TAKER_ALREADY_RECEIVED

    if body.is_accepted is True:
        await maker_dal.update({Maker.id: maker.id, Maker.is_accepted: True})
    else:
        await taker_dal.delete({Taker.id: maker.id})
