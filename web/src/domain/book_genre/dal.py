from uuid import UUID

from sqlalchemy import delete

from src.domain.abc.dal import ABCDAL
from src.domain.book_genre.model import BookGenre


class BookGenreDAL(ABCDAL[BookGenre]):
    async def delete_by_book(self, book_id: UUID):
        query = delete(
            self.model
        ).where(
            self.model.book_id == book_id
        )
        await self.session.execute(query)
