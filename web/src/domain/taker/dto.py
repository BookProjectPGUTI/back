from uuid import UUID

from pydantic import Field

from src.api.book.dto import BookResponse
from src.domain.abc.dto import ABCDTO
from src.domain.user.dto import UserShareDTO


class TakerDTO(ABCDTO):
    id: UUID = Field(..., description='ID тейкера')
    user: UserShareDTO = Field(..., description='Пользователь')
    book: BookResponse = Field(..., description='Книга')
    track_number: str | None = Field(None, max_length=48, description='Трек-номер')
    is_received: bool = Field(..., description='Подтверждение получение')


class TakerCreateDTO(ABCDTO):
    maker_id: UUID = Field(..., description='ID мейкера')
