import math
from typing import Annotated, Type, List, Dict, Any, Sequence, Sized

from sqlalchemy import insert, update, select, Select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Doc

from src.domain.abc.dto import PaginationDTO, PaginationInfoDTO
from src.domain.abc.model import ABCModel


class ABCDAL:
    """Абстракция для доступа к сущности с БД."""

    __slots__ = (
        'session',
        'pagination',
    )

    model: Annotated[
        Type[ABCModel],
        Doc(
            """
            Модель данных из бд. Через эту модель будут проводиться запросы.

            При наследовании обязательно нужно переопределить модель, иначе упадёт ошибка.

            Пример использования:
            ```python
            class EntityDAL(ABCDAL):
                model = Entity
            ```

            """
        ),
    ] = ABCModel

    def __init__(self, session: AsyncSession, pagination: PaginationDTO | None = None):
        self.pagination = None
        if pagination is not None:
            self.pagination = PaginationInfoDTO(
                page=pagination.page,
                page_size=pagination.page_size,
                page_count=0,
                total=0,
            )
        if not isinstance(session, AsyncSession):
            raise TypeError(f'"session" argument in {self.__class__.__name__} should be AsyncSession type.')

        if self.model is ABCDAL.model:
            msg = f'Class "{self.__class__.__name__}" is not override model class.\n'
            raise TypeError(msg)

        if not issubclass(self.model, ABCDAL.model):
            msg = f'"{self.model.__class__.__name__}" is not inhered from {ABCDAL.model.__class__.__name__}'
            raise TypeError(msg)

        self.session = session

    async def insert(self, data: List[Dict[str, Any]], return_value: bool = False) -> None | Sequence:
        if len(data) <= 0:
            return None
        if return_value:
            return (await self.session.scalars(
                insert(self.model).returning(self.model, sort_by_parameter_order=True),
                data
            )).all()
        else:
            await self.session.execute(insert(self.model), data)

    async def update(self, data: List[Dict[str, Any]]):
        if len(data) > 0:
            await self.session.execute(update(self.model), data)

    async def delete(self, ids: Sized):
        if not hasattr(self.model, 'id'):
            raise AttributeError('model has no attribute id')

        if len(ids) > 0:
            await self.session.execute(delete(self.model).where(self.model.id.in_(ids)))

    async def get_models(self) -> Sequence[ABCModel]:
        query = select(
            self.model
        )

        result = await self.session.scalars(query)
        return result.all()

    async def get_paginated_query(self, query: Select) -> Select:
        if self.pagination is None:
            raise ValueError(f'Cannot use pagination without {PaginationDTO.__name__} in __init__ params.')

        if self.pagination.page_count != 0 or self.pagination.total != 0:
            raise ValueError(f'This instance of {self.__class__.__name__} already used pagination.')

        pagination_query = select(
            func.count().label('total')
        ).select_from(
            query.subquery()
        )

        result = await self.session.execute(pagination_query)

        total = result.one().total
        self.pagination.total = total
        self.pagination.page_count = math.ceil(total / self.pagination.page_size)

        query = query.offset(
            (self.pagination.page - 1) * self.pagination.page_size
        ).limit(
            self.pagination.page_size
        )

        return query

    async def get_by_id(self, id_: str | int) -> model | None:
        clauses = []
        if hasattr(self.model, 'active'):
            clauses.append(self.model.active.is_(True))

        if not hasattr(self.model, 'id'):
            raise AttributeError('model has no attribute id')

        query = select(
            self.model
        ).where(
            self.model.id == id_,
            *clauses
        )

        return (await self.session.execute(query)).scalar_one_or_none()