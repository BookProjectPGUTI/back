from typing import List
from uuid import UUID

from pydantic import Field

from src.api.book.dto import BookResponse
from src.domain.abc.dto import ABCDTO
from src.domain.genre.dto import GenreDTO
from src.domain.user.dto import UserShareDTO


class MakerDTO(ABCDTO):
    id: UUID = Field(..., description='ID мейкера')
    is_accepted: bool = Field(..., description='Подтверждение обмена')
    is_received: bool = Field(..., description='Подтверждение получение')
    user: UserShareDTO = Field(..., description='Пользователь')
    book: BookResponse = Field(..., description='Книга')


class MakerMatchDTO(ABCDTO):
    id: UUID = Field(..., description='ID мейкера')
    user: UserShareDTO = Field(..., description='Пользователь')
    book: BookResponse = Field(..., description='Книга')
    taker_genre_matches: List[GenreDTO] = Field(..., description='Совпавшие жанры книги у тейкера')
    maker_genre_matches: List[GenreDTO] = Field(..., description='Совпавшие жанры книги у мейкера')


class MakerAcceptDTO(ABCDTO):
    is_accepted: bool = Field(description='Подтверждение обмена мейкером')
