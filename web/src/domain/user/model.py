import typing
import uuid

from sqlalchemy import func, UUID, VARCHAR, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCTimestampModel


class User(ABCTimestampModel):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=func.gen_random_uuid(), comment='Уникальный ID'
    )

    first_name: Mapped[str | None] = mapped_column(
        VARCHAR(25), nullable=True, comment='Имя пользователя'
    )

    last_name: Mapped[str | None] = mapped_column(
        VARCHAR(50), nullable=True, comment='Фамилия пользователя'
    )

    second_name: Mapped[str | None] = mapped_column(
        VARCHAR(25), nullable=True, comment='Отчество пользователя'
    )

    email: Mapped[str] = mapped_column(
        VARCHAR(60), nullable=False, unique=True, comment='Почта пользователя'
    )

    username: Mapped[str] = mapped_column(
        VARCHAR(20), nullable=False, unique=True, comment='Псевдоним пользователя'
    )

    password: Mapped[str] = mapped_column(
        VARCHAR(60), nullable=False, deferred=True, comment='SHA256 пароля пользователя'
    )

    is_confirmed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text('FALSE'), comment='Подтверждается ссылкой на почте'
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text('TRUE'), comment='Заблокирован ли пользователь'
    )

    genres: Mapped[typing.List['Genre']] = relationship(
        secondary='wish_list', back_populates='users'
    )

    genre_associations: Mapped[typing.List['WishList']] = relationship(
        back_populates='user', overlaps='users,genres'
    )

