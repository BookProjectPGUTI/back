from typing import List, Self

from pydantic import Field

from src.domain.abc.dto import ABCDTO
from src.utils.constansts import MAX_INT_32


class GenreDTO(ABCDTO):
    id: int = Field(..., ge=1, le=MAX_INT_32, description='Уникальный ID')
    name: str = Field(..., max_length=128, description='Название жанра')

    @classmethod
    def build_from_lists(cls, genre_ids: List[int], genre_names: List[str]) -> List[Self]:
        return [
            cls(
                id=genre_id,
                name=name,
            )
            for genre_id, name in zip(genre_ids, genre_names)
        ]
