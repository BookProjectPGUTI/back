from uuid import UUID

from sqlalchemy import select, and_, or_
from sqlalchemy.orm import joinedload

from src.api.book.dto import BookResponse
from src.domain.abc.dal import ABCDAL
from src.domain.author.dto import AuthorDTO
from src.domain.book.model import Book
from src.domain.genre.dto import GenreDTO
from src.domain.maker.model import Maker
from src.domain.taker.model import Taker


class BookDAL(ABCDAL[Book]):
    async def get_current_book(self, user_id: UUID) -> BookResponse | None:
        query = select(
            self.model
        ).options(
            joinedload(self.model.author),
            joinedload(self.model.genres),
        ).outerjoin(
            Maker, and_(
                Maker.book_id == self.model.id,
                Maker.is_received.is_(True),
            )
        ).outerjoin(
            Taker, and_(
                Taker.book_id == self.model.id,
                Taker.is_received.is_(True),
            )
        ).where(
            self.model.user_id == user_id,
            Taker.id.is_(None),
            Maker.id.is_(None),
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
