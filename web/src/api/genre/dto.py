from typing import List

from pydantic import Field

from src.domain.abc.dto import ABCResponse
from src.domain.genre.dto import GenreDTO


class GenreResponse(ABCResponse):
    genres: List[GenreDTO] = Field(..., description='Список жанров')
