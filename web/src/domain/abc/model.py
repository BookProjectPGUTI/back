import datetime
import abc
from typing import Any, Dict

from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ABCModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def __repr__(self):
        attrs = ', '.join(f"{key}={value}" for key, value in self.to_dict().items())
        return f'{self.__class__.__name__}({attrs})'

    def to_dict(self) -> Dict[str, Any]:
        return {
            field.name: getattr(self, field.name)
            for field in self.__table__.c  # noqa
        }


class ABCAdminModel(ABCModel):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), default=func.now(), onupdate=datetime.datetime.now, nullable=False
    )

    @abc.abstractmethod
    def __str__(self) -> str:
        ...
