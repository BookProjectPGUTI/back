from sqlalchemy.ext.asyncio import AsyncSession

from src.api.book.dto import BookCreateDTO, BookCreateResponse
from src.domain.auth.dto import AccessTokenDTO
from src.domain.author.dal import AuthorDAL
from src.domain.book.dal import BookDAL
from src.domain.book.model import Book
from src.domain.genre.dal import GenreDAL
from src.domain.genre.exception import GENRE_NOT_FOUND


async def create_book(
        session: AsyncSession, user_jwt: AccessTokenDTO, body: BookCreateDTO
) -> BookCreateResponse:
    author_dal = AuthorDAL(session)

    author = await author_dal.get_by_filter(body.author.model_dump())
    if author is None:
        author = await author_dal.insert(body.author.model_dump(), return_value=True)

    genres = await GenreDAL(session).get_many_by_filter(id=body.genres_ids)
    if len(genres) != len(body.genres_ids):
        raise GENRE_NOT_FOUND

    book = await BookDAL(session).insert(
        {
            Book.user_id.key: user_jwt.sub,
            Book.author_id.key: author.id,
            Book.name.key: body.name,
            Book.isbn.key: body.isbn,
            Book.published_year.key: body.publication_year,
            Book.genres.key: body.genres_ids,
        },
        return_value=True
    )

    return BookCreateResponse(
        id=book.id,
        author=author,
        name=book.name,
        isbn=book.isbn,
        publication_year=book.published_year,
        genres=genres,
    )
