import typing
import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.domain.abc.model import ABCTimestampModel


if typing.TYPE_CHECKING:
    from src.domain.user.model import User


def _user():
    from src.domain.user.model import User

    return User


class Token(ABCTimestampModel):
    __tablename__ = 'token'

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey(_user().id, ondelete='CASCADE'), primary_key=True, nullable=False, comment='ID пользователя'
    )

    refresh_id: Mapped[uuid.UUID] = mapped_column(
        UUID, nullable=False, comment='ID из jti refresh токена'
    )

    access_id: Mapped[uuid.UUID] = mapped_column(
        UUID, nullable=False, comment='ID из jti access токена'
    )

    user: Mapped[_user()] = relationship()

