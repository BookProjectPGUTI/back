from sqlalchemy.ext.asyncio import AsyncSession

from src.api.wish_list.dto import WishListCreateDTO, WishListResponse
from src.domain.auth.dto import AccessTokenDTO
from src.domain.genre.dal import GenreDAL
from src.domain.genre.exception import GENRE_NOT_FOUND
from src.domain.wish_list.dal import WishListDAL
from src.domain.wish_list.exception import WISH_LIST_NOT_FOUND
from src.domain.wish_list.model import WishList


async def create_wish_list(
        session: AsyncSession,
        user_jwt: AccessTokenDTO,
        body: WishListCreateDTO
) -> WishListResponse:
    genres = await GenreDAL(session).get_many_by_filter(id=body.genres_ids)
    if len(genres) != len(body.genres_ids):
        raise GENRE_NOT_FOUND

    wish_list_dal = WishListDAL(session)

    await wish_list_dal.delete_by_book(user_jwt.sub)
    await wish_list_dal.insert(
        [
            {
                WishList.user_id: user_jwt.sub,
                WishList.genre_id: genre_id
            }
            for genre_id in body.genres_ids
        ]
    )

    return WishListResponse(
        genres=genres
    )


async def get_wish_list(
        session: AsyncSession,
        user_jwt: AccessTokenDTO,
) -> WishListResponse:
    genres = await GenreDAL(session).get_by_user_id(user_jwt.sub)
    if len(genres) < 1:
        raise WISH_LIST_NOT_FOUND

    return WishListResponse(
        genres=genres
    )
