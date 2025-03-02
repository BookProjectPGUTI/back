from uuid import UUID

from pydantic import Field

from src.api.book.dto import BookResponse
from src.domain.abc.dto import ABCResponse


class MakerCreateResponse(ABCResponse):
    id: UUID = Field(..., description='Уникальный ID')
    book: BookResponse = Field(..., description='Книга для обмена')
