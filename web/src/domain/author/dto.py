from uuid import UUID

from pydantic import Field

from src.domain.abc.dto import ABCDTO


class AuthorCreateDTO(ABCDTO):
    first_name: str = Field(..., max_length=48, description='Имя автора')
    last_name: str = Field(..., max_length=48, description='Фамилия автора')


class AuthorDTO(ABCDTO):
    id: UUID = Field(..., description='Уникальный ID')
    first_name: str = Field(..., max_length=48, description='Имя автора')
    last_name: str = Field(..., max_length=48, description='Фамилия автора')
