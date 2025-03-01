import typing
import uuid

from sqlalchemy import func, UUID, VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCTimestampModel


if typing.TYPE_CHECKING:
    from src.domain.author.model import Author
    from src.domain.user.model import User


def _user():
    from src.domain.user.model import User

    return User


def _author():
    from src.domain.author.model import Author

    return Author


class Book(ABCTimestampModel):
    __tablename__ = 'book'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=func.gen_random_uuid(), comment='Уникальный ID'
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey(_user().id), nullable=False, comment='ID владельца книги'
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey(_author().id), nullable=False, comment='ID автора'
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, comment='Название книги'
    )

    isbn: Mapped[str] = mapped_column(
        VARCHAR(13), nullable=False, comment='ISBN номер книги'
    )

    published_year: Mapped[str] = mapped_column(
        VARCHAR(4), nullable=False, comment='Год публикации книги'
    )

    user: Mapped[_user()] = relationship()

    author: Mapped[_author()] = relationship()

    genres: Mapped[typing.List['Genre']] = relationship(
        secondary='book_genre', back_populates='books'
    )

    genre_associations: Mapped[typing.List['BookGenre']] = relationship(
        back_populates='book', overlaps='books,genres'
    )
