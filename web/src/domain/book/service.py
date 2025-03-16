from sqlalchemy.ext.asyncio import AsyncSession

from src.api.book.dto import BookCreateDTO, BookResponse
from src.domain.auth.dto import AccessTokenDTO
from src.domain.author.dal import AuthorDAL
from src.domain.author.exception import AUTHOR_NOT_FOUND
from src.domain.book.dal import BookDAL
from src.domain.book.exception import BOOK_NOT_FOUND, BOOK_ALREADY_EXISTS
from src.domain.book.model import Book
from src.domain.book_genre.dal import BookGenreDAL
from src.domain.book_genre.model import BookGenre
from src.domain.genre.dal import GenreDAL
from src.domain.genre.exception import GENRE_NOT_FOUND


async def create_book(
        session: AsyncSession, user_jwt: AccessTokenDTO, body: BookCreateDTO
) -> BookResponse:
    author_dal = AuthorDAL(session)

    author = await author_dal.get_by_filter(body.author.model_dump())
    if author is None:
        author = await author_dal.insert(body.author.model_dump(), return_value=True)

    if author is None:
        raise AUTHOR_NOT_FOUND

    genres = await GenreDAL(session).get_many_by_filter(id=body.genres_ids)
    if len(genres) != len(body.genres_ids):
        raise GENRE_NOT_FOUND

    book_dal = BookDAL(session)

    existing_book = await book_dal.get_current_book(user_jwt.sub)
    if existing_book is not None:
        raise BOOK_ALREADY_EXISTS

    book = await BookDAL(session).insert(
        {
            Book.user_id: user_jwt.sub,
            Book.author_id: author.id,
            Book.name: body.name,
            Book.isbn: body.isbn,
            Book.published_year: body.publication_year,
        },
        return_value=True
    )

    if book is None:
        raise BOOK_NOT_FOUND

    await BookGenreDAL(session).insert_many(
        [
            {
                BookGenre.book_id: book.id,
                BookGenre.genre_id: genre.id,
            }
            for genre in genres
        ]
    )

    return BookResponse(
        id=book.id,
        author=author,
        name=book.name,
        isbn=book.isbn,
        publication_year=book.published_year,
        genres=genres,
    )


async def get_book(session: AsyncSession, user_jwt: AccessTokenDTO) -> BookResponse:
    book = await BookDAL(session).get_current_book(user_jwt.sub)
    if book is None:
        raise BOOK_NOT_FOUND

    return book


async def update_book(session: AsyncSession, user_jwt: AccessTokenDTO, body: BookCreateDTO):
    book_dal = BookDAL(session)

    book = await book_dal.get_current_book(user_jwt.sub)
    if book is None:
        raise BOOK_NOT_FOUND

    author_dal = AuthorDAL(session)

    author = await author_dal.get_by_filter(body.author.model_dump())
    if author is None:
        author = await author_dal.insert(body.author.model_dump(), return_value=True)
    if author is None:
        raise AUTHOR_NOT_FOUND

    book_genre_dal = BookGenreDAL(session)
    await book_genre_dal.delete_by_book(book.id)
    await book_genre_dal.insert_many(
        [
            {
                BookGenre.book_id: book.id,
                BookGenre.genre_id: genre_id,
            }
            for genre_id in body.genres_ids
        ]
    )

    await book_dal.update(
        {
            Book.id: book.id,
            Book.user_id: user_jwt.sub,
            Book.author_id: author.id,
            Book.name: body.name,
            Book.isbn: body.isbn,
            Book.published_year: body.publication_year,
        }
    )
