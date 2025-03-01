from sqlalchemy import VARCHAR, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.abc.model import ABCTimestampModel


class Genre(ABCTimestampModel):
    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment='Уникальный ID'
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(128), nullable=False, unique=True, comment='Название жанра'
    )
