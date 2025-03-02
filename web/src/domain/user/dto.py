import re

from pydantic import Field, EmailStr

from src.domain.abc.dto import ABCDTO


class UserShareDTO(ABCDTO):
    first_name: str | None = Field(None, max_length=20, description='Имя пользователя')
    last_name: str | None = Field(None, max_length=50, description='Фамилия пользователя')
    second_name: str | None = Field(None, max_length=25, description='Отчество пользователя')
    username: str = Field(
        ...,
        max_length=20,
        pattern=re.compile(r'^[a-zA-Z0-9а-яА-ЯёЁ_\s-]+$'),
        description='Псевдоним пользователя'
    )
    rating: int = Field(0, ge=0, description='Рейтинг пользователя')
