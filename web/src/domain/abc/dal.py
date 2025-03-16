import math
from typing import Annotated, Generic, TypeVar, Type, Dict, Any, List, Sequence

from sqlalchemy import insert, update, delete, select, Select, func, BinaryExpression, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from typing_extensions import Doc

from src.domain.abc.dto import PaginationDTO, PaginationInfoDTO
from src.domain.abc.model import ABCModel

ModelType = TypeVar('ModelType', bound=ABCModel)

_DATA_ITEM_TYPE = (
    Dict[str, Any] |
    Dict[InstrumentedAttribute, Any] |
    Dict[str | InstrumentedAttribute, Any]
)

_DATA_LIST_TYPE = (
    List[Dict[str, Any]] |
    List[Dict[InstrumentedAttribute, Any]] |
    List[Dict[str | InstrumentedAttribute, Any]]
)

_DATA_TYPE = (
    _DATA_ITEM_TYPE |
    _DATA_LIST_TYPE
)


class ABCDAL(Generic[ModelType]):
    """Абстракция для доступа к сущности с БД."""

    __slots__ = (
        'session',
        'pagination',
    )

    model: Annotated[
        Type[ModelType],
        Doc(
            """
            Модель данных из бд. Через эту модель будут проводиться запросы.

            При наследовании обязательно нужно переопределить модель, иначе упадёт ошибка.

            Пример использования:
            ```python
            class EntityDAL(ABCDAL[Entity]):
                pass
            ```

            """
        ),
    ] = ABCModel  # type: ignore

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

        try:
            for orig_class in self.__orig_bases__:  # type: ignore
                for class_arg in orig_class.__args__:
                    if issubclass(class_arg, ABCDAL.model):  # type: ignore
                        self.model = class_arg  # type: ignore
        except AttributeError:
            pass
        except TypeError as e:
            e.add_note('The model was not passed on like this: class EntityDAL(ABCDAL[Entity]): ...')
            raise e

        if self.model == ABCDAL.model:  # type: ignore
            msg = 'The model was not passed on like this: class EntityDAL(ABCDAL[Entity]): ...'
            raise AttributeError(msg)

        self.session = session

    async def insert(
            self,
            data: _DATA_ITEM_TYPE,
            return_value: bool = False
    ) -> ModelType | None:
        self._validate_fields_exists(data)
        data_list: list[dict] = [data]

        if len(data_list) <= 0:
            return None

        params = self._build_params_from_data(data_list)

        if return_value:
            query = insert(
                self.model
            ).returning(
                self.model,
                sort_by_parameter_order=True
            )

            result = await self.session.scalars(query, params)
            return result.one()
        else:
            query = insert(
                self.model
            ).returning()

            await self.session.execute(query, params)
            return None

    async def insert_many(
            self,
            data: _DATA_LIST_TYPE,
            return_value: bool = False
    ) -> Sequence[ModelType] | None:
        for item in data:
            self._validate_fields_exists(item)

        if len(data) <= 0:
            return None

        params = self._build_params_from_data(data)

        if return_value:
            query = insert(
                self.model
            ).returning(
                self.model,
                sort_by_parameter_order=True
            )

            result = await self.session.scalars(query, params)
            items = result.all()
            return items
        else:
            query = insert(
                self.model
            ).returning()

            await self.session.execute(query, params)
            return None

    async def update(
            self,
            data: _DATA_TYPE,
    ):
        if isinstance(data, dict):
            self._validate_fields_exists(data)
            data_list: list[dict] = [data]
        else:
            for item in data:
                self._validate_fields_exists(item)
            data_list = data

        if len(data_list) <= 0:
            return None

        params = self._build_params_from_data(data_list)

        query = update(
            self.model
        )
        await self.session.execute(query, params)

    async def delete(
            self,
            filters: _DATA_ITEM_TYPE | None = None,
            **kwargs: Any,
    ):
        if filters is None:
            filters = {}

        filters.update(**kwargs)
        self._validate_fields_exists(filters)
        clauses = self._get_clauses_from_filters(filters)

        query = delete(
            self.model
        ).where(
            *clauses
        )

        await self.session.execute(query)

    async def get_models(self) -> Sequence[ModelType]:
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

    async def get_by_filter(
            self,
            filters: _DATA_ITEM_TYPE | None = None,
            **kwargs: Any,
    ) -> ModelType | None:
        if filters is None:
            filters = {}

        filters.update(**kwargs)
        self._validate_fields_exists(filters)
        clauses = self._get_clauses_from_filters(filters)

        query = select(
            self.model
        ).where(
            *clauses
        ).limit(1)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_many_by_filter(
            self,
            filters: _DATA_ITEM_TYPE | None = None,
            **kwargs: Any,
    ) -> Sequence[ModelType]:
        if filters is None:
            filters = {}

        filters.update(**kwargs)
        self._validate_fields_exists(filters)
        clauses = self._get_clauses_from_filters(filters)

        query = select(
            self.model
        ).where(
            *clauses
        )

        result = await self.session.scalars(query)
        return result.all()

    def _get_clauses_from_filters(self, filters: _DATA_ITEM_TYPE) -> List[BinaryExpression]:
        clauses = []
        for field, value in filters.items():
            if isinstance(field, InstrumentedAttribute):
                key = field.key
            else:
                key = field

            if value is None or isinstance(value, bool):
                clauses.append(getattr(self.model, key).is_(value))
            elif isinstance(value, (list, set, tuple)):
                clauses.append(getattr(self.model, key).in_(value))
            else:
                clauses.append(getattr(self.model, key) == value)

        return clauses

    def _validate_fields_exists(self, data: _DATA_ITEM_TYPE):
        model_inspect = inspect(self.model)
        attributes_names = {c_attr.key for c_attr in model_inspect.mapper.column_attrs}  # type: ignore

        invalid_attributes = {
            field.key
            if isinstance(field, InstrumentedAttribute) else
            field
            for field in data.keys()
        }.difference(attributes_names)
        if invalid_attributes:
            raise AttributeError(f'model has no attributes {invalid_attributes}')

    @staticmethod
    def _build_params_from_data(
            data: _DATA_LIST_TYPE
    ) -> List[Dict[str, Any]]:
        return [
            {
                field.key if isinstance(field, InstrumentedAttribute) else field: value
                for field, value in item.items()
            }
            for item in data
        ]

