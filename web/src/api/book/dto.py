import re
from typing import List, Set, Annotated
from uuid import UUID

from pydantic import Field, field_validator

from src.domain.abc.dto import ABCResponse, ABCDTO
from src.domain.author.dto import AuthorCreateDTO, AuthorDTO
from src.domain.genre.dto import GenreDTO
from src.utils.constansts import INT_32
from src.utils.time_utils import get_now


class BookCreateDTO(ABCDTO):
    author: AuthorCreateDTO = Field(..., description='Автор')
    name: str = Field(..., max_length=128, description='Название книги')
    isbn: str = Field(
        ...,
        max_length=13,
        pattern=re.compile(r'^(?:\d{9}[\dXx]|\d{13})$'),
        description='ISBN книги (ISBN-10 или ISBN-13)',
    )
    publication_year: str = Field(
        ...,
        max_length=4,
        pattern=re.compile(r'^(1[0-9]{3}|20[0-9]{2})$'),
        description='Год выпуска книги (от 1000 до 2099)',
    )
    genres_ids: Annotated[Set[int], INT_32] = Field(
        ..., min_length=1, description='Список ID жанров книги'
    )

    @field_validator('publication_year', mode='after')
    @classmethod
    def publication_year_validator(cls, v: str) -> str:
        if int(v) > get_now().year:
            raise ValueError('Год должен быть меньше или равен текущему.')
        return v


class BookResponse(ABCResponse):
    id: UUID = Field(..., description='Уникальный ID')
    author: AuthorDTO = Field(..., description='Автор')
    name: str = Field(..., max_length=128, description='Название книги')
    isbn: str = Field(
        ...,
        max_length=13,
        pattern=re.compile(r'^(?:\d{9}[\dXx]|\d{13})$'),
        description='ISBN книги (ISBN-10 или ISBN-13)',
    )
    publication_year: str = Field(
        ...,
        max_length=4,
        pattern=re.compile(r'^(1[0-9]{3}|20[0-9]{2})$'),
        description='Год выпуска книги (от 1000 до 2099)',
    )
    genres: List[GenreDTO] = Field(..., min_length=1, description='Жанры книги')

    @field_validator('publication_year', mode='after')
    @classmethod
    def publication_year_validator(cls, v: str) -> str:
        if int(v) > get_now().year:
            raise ValueError('Год должен быть меньше или равен текущему.')
        return v


class BookMatchDTO(ABCDTO):
    id: UUID = Field(..., description='Уникальный ID')
    author: AuthorDTO = Field(..., description='Автор')
    name: str = Field(..., max_length=128, description='Название книги')
    isbn: str = Field(
        ...,
        max_length=13,
        pattern=re.compile(r'^(?:\d{9}[\dXx]|\d{13})$'),
        description='ISBN книги (ISBN-10 или ISBN-13)',
    )
    publication_year: str = Field(
        ...,
        max_length=4,
        pattern=re.compile(r'^(1[0-9]{3}|20[0-9]{2})$'),
        description='Год выпуска книги (от 1000 до 2099)',
    )
    genres: List[GenreDTO] = Field(..., min_length=1, description='Жанры книги')

    @field_validator('publication_year', mode='after')
    @classmethod
    def publication_year_validator(cls, v: str) -> str:
        if int(v) > get_now().year:
            raise ValueError('Год должен быть меньше или равен текущему.')
        return v
