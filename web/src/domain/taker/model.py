import typing
import uuid

from sqlalchemy import UUID, VARCHAR, ForeignKey, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCTimestampModel


if typing.TYPE_CHECKING:
    from src.domain.user.model import User
    from src.domain.book.model import Book


def _user():
    from src.domain.user.model import User

    return User


def _book():
    from src.domain.book.model import Book

    return Book


class Taker(ABCTimestampModel):
    __tablename__ = 'taker'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey('maker.id'), primary_key=True, comment='Уникальный ID'
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey(_user().id), nullable=False, comment='ID пользователя'
    )

    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey(_book().id), nullable=False, comment='ID книги'
    )

    track_number: Mapped[str] = mapped_column(
        VARCHAR(48), nullable=True, comment='Номер отслеживания посылки'
    )

    is_received: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text('FALSE'), comment='Подтверждение получения книги'
    )

    user: Mapped[_user()] = relationship()  # type: ignore
    book: Mapped[_book()] = relationship()  # type: ignore
    maker: Mapped['Maker'] = relationship(back_populates='taker')  # type: ignore
