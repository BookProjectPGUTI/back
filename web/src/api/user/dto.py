import re
from typing import List
from uuid import UUID

from pydantic import EmailStr, Field

from src.domain.abc.dto import ABCResponse, ABCDTO
from src.domain.user_address.dto import UserAddressDTO


class UserResponse(ABCResponse):
    id: UUID = Field(..., description='ID пользователя')
    first_name: str | None = Field(None, max_length=20, description='Имя пользователя')
    last_name: str | None = Field(None, max_length=50, description='Фамилия пользователя')
    second_name: str | None = Field(None, max_length=25, description='Отчество пользователя')
    email: EmailStr = Field(..., max_length=60, description='Почта пользователя')
    username: str = Field(
        ..., max_length=20, pattern=re.compile(r'^[a-zA-Z0-9а-яА-ЯёЁ_\s-]+$'),
        description='Псевдоним пользователя'
    )
    rating: int = Field(0, ge=0, description='Рейтинг пользователя')


class UserNameDTO(ABCDTO):
    first_name: str = Field(..., max_length=20, description='Имя пользователя')
    last_name: str = Field(..., max_length=50, description='Фамилия пользователя')
    second_name: str = Field(..., max_length=25, description='Отчество пользователя')


class UserAddressCreateDTO(ABCDTO):
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


class UserAddressResponse(ABCResponse):
    addresses: List[UserAddressDTO] = Field(..., description='Список адресов')
