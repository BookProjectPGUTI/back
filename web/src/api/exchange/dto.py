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


class MakerResponse(ABCResponse):
    makers: List[MakerMatchDTO] = Field(..., description='Предложения по обмену')


class TakerDTO(ABCDTO):
    id: UUID = Field(..., description='ID тейкера')
    user: UserShareDTO = Field(..., description='Пользователь')
    book: BookResponse = Field(..., description='Книга')
    is_received: bool = Field(..., description='Подтверждение получение')


class ExchangeResponse(ABCResponse):
    maker: MakerDTO = Field(..., description='Мейкер')
    taker: TakerDTO | None = Field(..., description='Тейкер')
    taker_genre_matches: List[GenreDTO] = Field(..., description='Совпавшие жанры книги у тейкера')
    maker_genre_matches: List[GenreDTO] = Field(..., description='Совпавшие жанры книги у мейкера')
