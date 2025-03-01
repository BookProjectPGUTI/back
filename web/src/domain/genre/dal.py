from uuid import UUID
from typing import Sequence

from sqlalchemy import select, and_

from src.domain.abc.dal import ABCDAL
from src.domain.genre.model import Genre
from src.domain.wish_list.model import WishList


class GenreDAL(ABCDAL[Genre]):
    async def get_by_user_id(self, user_id: UUID) -> Sequence[Genre]:
        query = select(
            self.model
        ).join(
            WishList,
            and_(
                WishList.genre_id == self.model.id,
                WishList.user_id == user_id
            )
        )

        result = await self.session.scalars(query)
        return result.all()
