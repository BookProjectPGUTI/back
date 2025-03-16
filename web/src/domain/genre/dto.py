from typing import List, Self, Annotated

from pydantic import Field

from src.domain.abc.dto import ABCDTO
from src.utils.constansts import INT_32


class GenreDTO(ABCDTO):
    id: Annotated[int, INT_32] = Field(..., description='Уникальный ID')
    name: str = Field(..., max_length=128, description='Название жанра')

    @classmethod
    def build_from_lists(cls, genre_ids: List[int] | None, genre_names: List[str] | None) -> List[Self]:
        if genre_ids is None or genre_names is None:
            return []
        return [
            cls(
                id=genre_id,
                name=name,
            )
            for genre_id, name in zip(genre_ids, genre_names)
        ]
