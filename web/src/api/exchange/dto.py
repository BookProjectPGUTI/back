from typing import List
from uuid import UUID

from pydantic import Field

from src.api.book.dto import BookResponse
from src.domain.abc.dto import ABCResponse
from src.domain.genre.dto import GenreDTO
from src.domain.maker.dto import MakerDTO, MakerMatchDTO
from src.domain.taker.dto import TakerDTO


class MakerCreateResponse(ABCResponse):
    id: UUID = Field(..., description='Уникальный ID')
    book: BookResponse = Field(..., description='Книга для обмена')


class MakerResponse(ABCResponse):
    makers: List[MakerMatchDTO] = Field(..., description='Предложения по обмену')


class ExchangeResponse(ABCResponse):
    maker: MakerDTO = Field(..., description='Мейкер')
    taker: TakerDTO | None = Field(..., description='Тейкер')
    taker_genre_matches: List[GenreDTO] = Field(..., description='Совпавшие жанры книги у тейкера')
    maker_genre_matches: List[GenreDTO] = Field(..., description='Совпавшие жанры книги у мейкера')


class TakerCreateResponse(ABCResponse):
    detail: str = Field(
        'Вы определили пару для обмена. Ожидаем подтверждения обмена от Мейкера.',
        description='Описание ответа'
    )
