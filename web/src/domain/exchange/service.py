from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth.dto import AccessTokenDTO
from src.domain.book.dal import BookDAL
from src.domain.book.exception import BOOK_NOT_FOUND
from src.domain.book_genre.dal import BookGenreDAL
from src.domain.book_genre.exception import BOOK_GENRE_NOT_FOUND
from src.domain.book_genre.model import BookGenre
from src.domain.maker.dal import MakerDAL
from src.domain.maker.exception import MAKER_ALREADY_EXISTS
from src.domain.maker.model import Maker
from src.domain.taker.dal import TakerDAL
from src.domain.taker.exception import TAKER_ALREADY_EXISTS
from src.domain.taker.model import Taker
from src.domain.user.dal import UserDAL
from src.domain.user.exception import USER_NOT_FOUND, USER_NOT_NAMED
from src.domain.user_address.dal import UserAddressDAL
from src.domain.user_address.exception import USER_ADDRESS_NOT_FOUND
from src.domain.user_address.model import UserAddress
from src.domain.wish_list.dal import WishListDAL
from src.domain.wish_list.exception import WISH_LIST_NOT_FOUND
from src.domain.wish_list.model import WishList


async def validate_user_can_edit_setup(session: AsyncSession, user: AccessTokenDTO):
    maker_dal = MakerDAL(session)
    taker_dal = TakerDAL(session)

    active_maker = await maker_dal.get_by_filter(
        {
            Maker.user_id: user.sub,
            Maker.is_received: False,
        }
    )
    if active_maker is not None:
        raise MAKER_ALREADY_EXISTS

    active_taker = await taker_dal.get_by_filter(
        {
            Taker.user_id: user.sub,
            Taker.is_received: False,
        }
    )
    if active_taker is not None:
        raise TAKER_ALREADY_EXISTS


async def validate_user_complete_setup(session: AsyncSession, user: AccessTokenDTO):
    book_dal = BookDAL(session)
    book_genre_dal = BookGenreDAL(session)
    user_dal = UserDAL(session)
    user_address_dal = UserAddressDAL(session)
    wish_list_dal = WishListDAL(session)

    book = await book_dal.get_current_book(user.sub)
    if book is None:
        raise BOOK_NOT_FOUND

    book_genres = await book_genre_dal.get_many_by_filter(
        {
            BookGenre.book_id: book.id
        }
    )
    if len(book_genres) < 1:
        raise BOOK_GENRE_NOT_FOUND

    user_db = await user_dal.get_by_filter(id=user.sub)
    if user_db is None:
        raise USER_NOT_FOUND
    if (
            user_db.first_name is None or
            user_db.second_name is None or
            user_db.last_name is None
    ):
        raise USER_NOT_NAMED

    user_address = await user_address_dal.get_many_by_filter(
        {
            UserAddress.user_id: user.sub,
            UserAddress.is_active: True,
        }
    )
    if user_address is None:
        raise USER_ADDRESS_NOT_FOUND

    wish_list = await wish_list_dal.get_many_by_filter(
        {
            WishList.user_id: user.sub
        }
    )
    if len(wish_list) < 1:
        raise WISH_LIST_NOT_FOUND
