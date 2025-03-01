from typing import List, Set

from pydantic import Field, conint

from src.domain.abc.dto import ABCDTO, ABCResponse
from src.domain.genre.dto import GenreDTO
from src.utils.constansts import MAX_INT_32


class WishListCreateDTO(ABCDTO):
    genres_ids: Set[conint(ge=1, le=MAX_INT_32)] = Field(
        ..., min_items=1, description='Список ID жанров книги'
    )


class WishListResponse(ABCResponse):
    genres: List[GenreDTO] = Field(..., min_items=1, description='Жанры книги')
