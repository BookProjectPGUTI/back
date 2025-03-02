from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exchange.dto import MakerCreateResponse, MakerResponse
from src.domain.auth.dto import AccessTokenDTO
from src.domain.book.dal import BookDAL
from src.domain.book.exception import BOOK_NOT_FOUND
from src.domain.maker.dal import MakerDAL
from src.domain.maker.model import Maker
from src.domain.user.dal import UserDAL
from src.domain.user.exception import USER_NOT_NAMED
from src.domain.user_address.dal import UserAddressDAL
from src.domain.user_address.exception import USER_ADDRESS_NOT_FOUND
from src.domain.user_address.model import UserAddress


async def create_maker(
        user: AccessTokenDTO,
        session: AsyncSession
) -> MakerCreateResponse:
    maker_dal = MakerDAL(session)
    book_dal = BookDAL(session)
    user_dal = UserDAL(session)
    user_address_dal = UserAddressDAL(session)

    book = await book_dal.get_current_book(user.sub)
    if book is None:
        raise BOOK_NOT_FOUND

    user_db = await user_dal.get_by_filter(id=user.sub)
    if (
            user_db.first_name is None or
            user_db.second_name is None or
            user_db.last_name is None
    ):
        raise USER_NOT_NAMED

    user_address = await user_address_dal.get_many_by_filter(
        {
            UserAddress.user_id.key: user.sub,
            UserAddress.is_active.key: True,
        }
    )
    if user_address is None:
        raise USER_ADDRESS_NOT_FOUND

    maker = await maker_dal.insert(
        {
            Maker.user_id.key: user.sub,
            Maker.book_id.key: book.id,
        },
        return_value=True
    )

    return MakerCreateResponse(
        id=maker.id,
        book=book,
    )


async def get_makers(
        user: AccessTokenDTO,
        session: AsyncSession
) -> MakerResponse:
    maker_dal = MakerDAL(session)
    book_dal = BookDAL(session)
    user_dal = UserDAL(session)
    user_address_dal = UserAddressDAL(session)

    book = await book_dal.get_current_book(user.sub)
    if book is None:
        raise BOOK_NOT_FOUND

    user_db = await user_dal.get_by_filter(id=user.sub)
    if (
            user_db.first_name is None or
            user_db.second_name is None or
            user_db.last_name is None
    ):
        raise USER_NOT_NAMED

    user_address = await user_address_dal.get_many_by_filter(
        {
            UserAddress.user_id.key: user.sub,
            UserAddress.is_active.key: True,
        }
    )
    if user_address is None:
        raise USER_ADDRESS_NOT_FOUND

    makers = await maker_dal.get_matched_makers(user.sub)

    return MakerResponse(
        makers=makers
    )
