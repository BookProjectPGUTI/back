import typing
from typing import List

from sqlalchemy import VARCHAR, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCTimestampModel

if typing.TYPE_CHECKING:
    from src.domain.book.model import Book
    from src.domain.book_genre.model import BookGenre
    from src.domain.user.model import User
    from src.domain.wish_list.model import WishList



class Genre(ABCTimestampModel):
    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment='Уникальный ID'
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, unique=True, comment='Название жанра'
    )

    books: Mapped[List['Book']] = relationship(
        secondary='book_genre', back_populates='genres'
    )

    book_associations: Mapped[List['BookGenre']] = relationship(
        back_populates='genre', overlaps='books,genres'
    )

    users: Mapped[List['User']] = relationship(
        secondary='wish_list', back_populates='genres'
    )

    user_associations: Mapped[List['WishList']] = relationship(
        back_populates='genre', overlaps='users,genres'
    )
