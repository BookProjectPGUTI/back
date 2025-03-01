from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.api.book.dto import BookResponse
from src.domain.abc.dal import ABCDAL
from src.domain.author.dto import AuthorDTO
from src.domain.book.model import Book
from src.domain.genre.dto import GenreDTO


class BookDAL(ABCDAL[Book]):
    async def get_current_book(self, user_id: UUID) -> BookResponse | None:
        query = select(
            self.model
        ).options(
            joinedload(self.model.author),
            joinedload(self.model.genres),
        ).where(
            self.model.user_id == user_id
        ).order_by(
            self.model.updated_at.desc()
        ).limit(1)

        result = (await self.session.execute(query)).unique().scalar_one_or_none()
        if result is None:
            return None
        else:
            return BookResponse(
                id=result.id,
                author=AuthorDTO.model_validate(result.author),
                name=result.name,
                isbn=result.isbn,
                publication_year=result.published_year,
                genres=[
                    GenreDTO.model_validate(item)
                    for item in result.genres
                ]
            )
