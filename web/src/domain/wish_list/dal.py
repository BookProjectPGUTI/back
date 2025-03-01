from uuid import UUID

from sqlalchemy import delete

from src.domain.abc.dal import ABCDAL
from src.domain.wish_list.model import WishList


class WishListDAL(ABCDAL[WishList]):
    async def delete_by_book(self, user_id: UUID):
        query = delete(
            self.model
        ).where(
            self.model.user_id == user_id
        )
        await self.session.execute(query)
