import uuid

from sqlalchemy import UUID, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.abc.model import ABCTimestampModel


class WishList(ABCTimestampModel):
    __tablename__ = 'wish_list'

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey('user.id'), primary_key=True, comment='ID пользователя'
    )
    genre_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('genre.id'), primary_key=True, comment='ID жанра'
    )

    genre: Mapped['Genre'] = relationship(  # type: ignore
        back_populates='user_associations', overlaps='users,genres'
    )

    user: Mapped['User'] = relationship(  # type: ignore
        back_populates='genre_associations', overlaps='users,genres'
    )
