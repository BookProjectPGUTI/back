import typing
import uuid

from sqlalchemy import func, UUID, VARCHAR, ForeignKey, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCTimestampModel


if typing.TYPE_CHECKING:
    from src.domain.user.model import User
    from src.domain.book.model import Book
    from src.domain.taker.model import Taker


def _user():
    from src.domain.user.model import User

    return User


def _book():
    from src.domain.book.model import Book

    return Book


class Maker(ABCTimestampModel):
    __tablename__ = 'maker'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=func.gen_random_uuid(), comment='Уникальный ID'
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

    is_accepted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text('FALSE'), comment='Подтверждение начала обмена'
    )

    user: Mapped['User'] = relationship()
    book: Mapped['Book'] = relationship()
    taker: Mapped['Taker'] = relationship(back_populates='maker')
