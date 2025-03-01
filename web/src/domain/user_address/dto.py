import re
from uuid import UUID

from pydantic import Field

from src.domain.abc.dto import ABCDTO


class UserAddressDTO(ABCDTO):
    id: UUID = Field(..., description='Уникальный ID')
    user_id: UUID = Field(..., description='ID пользователя')
    mail_index: str = Field(
        ...,
        max_length=6,
        min_length=6,
        pattern=re.compile(r'^\d{6}$'),
        description='Почтовый индекс'
    )
    city: str = Field(
        ...,
        max_length=128,
        pattern=re.compile(r'^[А-Яа-яЁё\s-]+$'),
        description='Название города',
        examples=['Самара']
    )
    street: str = Field(
        ...,
        max_length=128,
        pattern=re.compile(r'^[А-Яа-яЁё\s-]+$'),
        description='Название улицы',
        examples=['Ленинградская улица']
    )
    house: str | None = Field(
        None,
        max_length=128,
        pattern=re.compile(r'^\d+[А-Яа-яЁё]?$'),
        description='Номер дома',
        examples=['111а']
    )
    build: str | None = Field(
        None,
        max_length=128,
        pattern=re.compile(r'^\d+[А-Яа-яЁё]?$'),
        description='Номер строения',
        examples=['5']
    )
    apartment: str = Field(
        ...,
        max_length=128,
        pattern=re.compile(r'^\d+$'),
        description='Номер квартиры',
        examples=['45']
    )
    is_active: bool = Field(True, description='Активность адреса')
