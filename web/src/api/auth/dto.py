import re
from uuid import UUID

from pydantic import EmailStr, Field

from src.domain.abc.dto import ABCDTO, ABCResponse


class SignUpDTO(ABCDTO):
    email: EmailStr = Field(..., max_length=60, description='Почта пользователя')
    username: str = Field(
        ..., max_length=20, pattern=re.compile(r'^[a-zA-Z0-9а-яА-ЯёЁ_\s-]+$'),
        description='Псевдоним пользователя'
    )
    password: str = Field(
        ..., min_length=8, max_length=60, pattern=re.compile(r'^(?=.*[A-Z])(?=.*\d).+$'),
        description='Пароль пользователя'
    )


class SignUpResponse(ABCResponse):
    detail: str = Field('Регистрация прошла успешно! Проверьте email для подтверждения.')


class SignInDTO(ABCDTO):
    username: str = Field(..., max_length=20, description='Псевдоним пользователя')
    password: str = Field(..., min_length=8, max_length=60, description='Пароль пользователя')


class SingInResponse(ABCResponse):
    id: UUID = Field(..., description='ID пользователя')
    username: str = Field(..., max_length=20, description='Псевдоним пользователя')
    email: EmailStr = Field(..., max_length=60, description='Почта пользователя')
