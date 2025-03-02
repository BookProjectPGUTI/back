from typing import List
from uuid import UUID

from pydantic import Field

from src.api.book.dto import BookResponse
from src.domain.abc.dto import ABCResponse, ABCDTO
from src.domain.genre.dto import GenreDTO
from src.domain.user.dto import UserShareDTO


class MakerCreateResponse(ABCResponse):
    id: UUID = Field(..., description='Уникальный ID')
    book: BookResponse = Field(..., description='Книга для обмена')


class MakerDTO(ABCDTO):
    id: UUID = Field(..., description='ID мейкера')
    user: UserShareDTO = Field(..., description='Пользователь')
    book: BookResponse = Field(..., description='Книга')
    taker_genre_matches: List[GenreDTO] = Field(..., min_items=0, description='Совпавшие жанры книги у тейкера')
    maker_genre_matches: List[GenreDTO] = Field(..., min_items=0, description='Совпавшие жанры книги у мейкера')


class MakerResponse(ABCResponse):
    makers: List[MakerDTO] = Field(..., description='Предложения по обмену')
