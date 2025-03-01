from sqlalchemy.ext.asyncio import AsyncSession

from src.api.wish_list.dto import WishListCreateDTO, WishListResponse
from src.domain.auth.dto import AccessTokenDTO
from src.domain.genre.dal import GenreDAL
from src.domain.genre.exception import GENRE_NOT_FOUND
from src.domain.wish_list.dal import WishListDAL
from src.domain.wish_list.model import WishList


async def create_wish_list(
        session: AsyncSession,
        user_jwt: AccessTokenDTO,
        body: WishListCreateDTO
) -> WishListResponse:
    genres = await GenreDAL(session).get_many_by_filter(id=body.genres_ids)
    if len(genres) != len(body.genres_ids):
        raise GENRE_NOT_FOUND

    await WishListDAL(session).delete_by_book(user_jwt.sub)
    await WishListDAL(session).insert(
        [
            {
                WishList.user_id.key: user_jwt.sub,
                WishList.genre_id.key: genre_id
            }
            for genre_id in body.genres_ids
        ]
    )

    return WishListResponse(
        genres=genres
    )
