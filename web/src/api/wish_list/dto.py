from typing import List, Set, Annotated

from pydantic import Field

from src.domain.abc.dto import ABCDTO, ABCResponse
from src.domain.genre.dto import GenreDTO
from src.utils.constansts import INT_32


class WishListCreateDTO(ABCDTO):
    genres_ids: Annotated[Set[int], INT_32] = Field(
        ..., min_length=1, description='Список ID жанров книги'
    )


class WishListResponse(ABCResponse):
    genres: List[GenreDTO] = Field(..., min_length=1, description='Жанры книги')
