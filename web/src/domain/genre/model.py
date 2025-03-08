from typing import List

from sqlalchemy import VARCHAR, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCTimestampModel


class Genre(ABCTimestampModel):
    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment='Уникальный ID'
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, unique=True, comment='Название жанра'
    )

    books: Mapped[List['Book']] = relationship(  # type: ignore
        secondary='book_genre', back_populates='genres'
    )

    book_associations: Mapped[List['BookGenre']] = relationship(  # type: ignore
        back_populates='genre', overlaps='books,genres'
    )

    users: Mapped[List['User']] = relationship(  # type: ignore
        secondary='wish_list', back_populates='genres'
    )

    user_associations: Mapped[List['WishList']] = relationship(  # type: ignore
        back_populates='genre', overlaps='users,genres'
    )
