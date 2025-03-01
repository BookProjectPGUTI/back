from sqlalchemy.ext.asyncio import AsyncSession

from src.api.genre.dto import GenreResponse
from src.domain.genre.dal import GenreDAL


async def get_genres(session: AsyncSession) -> GenreResponse:
    genres = await GenreDAL(session).get_models()

    return GenreResponse(
        genres=genres
    )
