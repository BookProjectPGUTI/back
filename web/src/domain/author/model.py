import uuid

from sqlalchemy import VARCHAR, func, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.abc.model import ABCTimestampModel


class Author(ABCTimestampModel):
    __tablename__ = 'author'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, server_default=func.gen_random_uuid(), comment='Уникальный ID'
    )

    first_name: Mapped[str | None] = mapped_column(
        VARCHAR(48), nullable=True, comment='Имя автора'
    )

    last_name: Mapped[str | None] = mapped_column(
        VARCHAR(48), nullable=True, comment='Фамилия автора'
    )
