import uuid

from sqlalchemy import UUID, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCModel


class BookGenre(ABCModel):
    __tablename__ = 'book_genre'

    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey('book.id'), primary_key=True, comment='ID книги'
    )
    genre_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('genre.id'), primary_key=True, comment='ID жанра'
    )

    genre: Mapped['Genre'] = relationship(
        back_populates='book_associations', overlaps='books,genres'
    )

    book: Mapped['Book'] = relationship(
        back_populates='genre_associations', overlaps='books,genres'
    )
