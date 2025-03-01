from pydantic import Field

from src.domain.abc.dto import ABCDTO
from src.utils.constansts import MAX_INT_32


class GenreDTO(ABCDTO):
    id: int = Field(..., ge=1, le=MAX_INT_32, description='Уникальный ID')
    name: str = Field(..., max_length=128, description='Название жанра')
