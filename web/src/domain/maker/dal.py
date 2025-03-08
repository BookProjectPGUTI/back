from typing import List
from uuid import UUID

from sqlalchemy import select, func, ScalarSelect, or_, FunctionFilter
from sqlalchemy.orm import aliased, InstrumentedAttribute

from src.api.book.dto import BookResponse
from src.api.exchange.dto import MakerMatchDTO, ExchangeResponse, MakerDTO, TakerDTO
from src.domain.abc.dal import ABCDAL
from src.domain.author.model import Author
from src.domain.book.model import Book
from src.domain.book_genre.model import BookGenre
from src.domain.genre.dto import GenreDTO
from src.domain.genre.model import Genre
from src.domain.maker.model import Maker
from src.domain.taker.model import Taker
from src.domain.user.model import User
from src.domain.wish_list.model import WishList


class MakerDAL(ABCDAL[Maker]):
    async def get_matched_makers(self, user_id: UUID) -> List[MakerMatchDTO]:
        def _build_array_query(
                field: InstrumentedAttribute,
                genre_query: ScalarSelect
        ) -> FunctionFilter:
            return func.array_agg(
                field
            ).filter(
                GenreAlias.id.in_(genre_query)
            )

        GenreAlias = aliased(Genre)

        maker_genre_subquery = select(
            BookGenre.genre_id
        ).where(
            BookGenre.book_id == self.model.book_id
        ).scalar_subquery()

        book_genre_ids_subquery = _build_array_query(GenreAlias.id, maker_genre_subquery)
        book_genre_names_subquery = _build_array_query(GenreAlias.name, maker_genre_subquery)

        taker_matches_subquery = select(
            WishList.genre_id
        ).where(
            WishList.user_id == user_id
        ).scalar_subquery()

        taker_match_count_subquery = func.count(
            GenreAlias.id
        ).filter(
            GenreAlias.id.in_(taker_matches_subquery)
        )

        taker_matched_ids_subquery = _build_array_query(GenreAlias.id, taker_matches_subquery)
        taker_matched_names_subquery = _build_array_query(GenreAlias.name, taker_matches_subquery)

        maker_matches_subquery = select(
            WishList.genre_id
        ).where(
            WishList.user_id == self.model.user_id
        ).scalar_subquery()

        maker_match_count_subquery = func.count(
            GenreAlias.id
        ).filter(
            GenreAlias.id.in_(maker_matches_subquery)
        )

        maker_matched_ids_subquery = _build_array_query(GenreAlias.id, maker_matches_subquery)
        maker_matched_names_subquery = _build_array_query(GenreAlias.name, maker_matches_subquery)

        query = select(
            self.model,
            Book,
            Author,
            User,
            book_genre_ids_subquery.label('book_genre_ids'),
            book_genre_names_subquery.label('book_genre_names'),
            taker_matched_ids_subquery.label('taker_matched_ids'),
            taker_matched_names_subquery.label('taker_matched_names'),
            maker_matched_ids_subquery.label('maker_matched_ids'),
            maker_matched_names_subquery.label('maker_matched_names'),
        ).join(
            Book,
            Book.id == self.model.book_id
        ).join(
            Author,
            Book.author
        ).join(
            User,
            self.model.user
        ).join(
            GenreAlias,
            Book.genres
        ).where(
            self.model.is_accepted.is_(False),
            self.model.is_received.is_(False),
            self.model.user_id != user_id
        ).group_by(
            self.model.id,
            Book.id,
            Author.id,
            User.id,
        ).order_by(
            taker_match_count_subquery.desc(),
            maker_match_count_subquery.desc(),
        )

        result = await self.session.execute(query)
        return [
            MakerMatchDTO(
                id=maker.id,
                user=maker.user,
                book=BookResponse(
                    id=book.id,
                    author=author,
                    name=book.name,
                    isbn=book.isbn,
                    publication_year=book.published_year,
                    genres=GenreDTO.build_from_lists(book_genre_ids, book_genre_names),
                ),
                taker_genre_matches=GenreDTO.build_from_lists(taker_matched_ids, taker_matched_names),
                maker_genre_matches=GenreDTO.build_from_lists(maker_matched_ids, maker_matched_names),
            )
            for (
                    maker,
                    book,
                    author,
                    user,
                    book_genre_ids,
                    book_genre_names,
                    taker_matched_ids,
                    taker_matched_names,
                    maker_matched_ids,
                    maker_matched_names,
            ) in result.all()
        ]

    async def get_current_maker(self, user_id: UUID) -> ExchangeResponse | None:
        def _build_array_query(
                field: InstrumentedAttribute,
                genre_query: ScalarSelect
        ) -> FunctionFilter:
            return func.array_agg(
                field
            ).filter(
                GenreAlias.id.in_(genre_query)
            )

        GenreAlias = aliased(Genre)

        maker_genre_subquery = select(
            BookGenre.genre_id
        ).where(
            BookGenre.book_id == self.model.book_id
        ).scalar_subquery()

        book_genre_ids_subquery = _build_array_query(GenreAlias.id, maker_genre_subquery)
        book_genre_names_subquery = _build_array_query(GenreAlias.name, maker_genre_subquery)

        taker_matches_subquery = select(
            WishList.genre_id
        ).where(
            WishList.user_id == user_id
        ).scalar_subquery()

        taker_match_count_subquery = func.count(
            GenreAlias.id
        ).filter(
            GenreAlias.id.in_(taker_matches_subquery)
        )

        taker_matched_ids_subquery = _build_array_query(GenreAlias.id, taker_matches_subquery)
        taker_matched_names_subquery = _build_array_query(GenreAlias.name, taker_matches_subquery)

        maker_matches_subquery = select(
            WishList.genre_id
        ).where(
            WishList.user_id == self.model.user_id
        ).scalar_subquery()

        maker_match_count_subquery = func.count(
            GenreAlias.id
        ).filter(
            GenreAlias.id.in_(maker_matches_subquery)
        )

        maker_matched_ids_subquery = _build_array_query(GenreAlias.id, maker_matches_subquery)
        maker_matched_names_subquery = _build_array_query(GenreAlias.name, maker_matches_subquery)

        TakerBook = aliased(Book)
        TakerUser = aliased(User)
        TakerAuthor = aliased(Author)
        TakerGenre = aliased(Genre)
        TakerBookGenre = aliased(BookGenre)

        taker_genre_subquery = select(
            TakerBookGenre.genre_id
        ).where(
            TakerBookGenre.book_id == self.model.book_id
        ).scalar_subquery()

        taker_book_genre_ids_subquery = _build_array_query(TakerGenre.id, taker_genre_subquery)
        taker_book_genre_names_subquery = _build_array_query(TakerGenre.name, taker_genre_subquery)

        query = select(
            self.model,
            Book,
            Author,
            User,
            Taker,
            TakerBook,
            TakerAuthor,
            TakerUser,
            book_genre_ids_subquery.label('book_genre_ids'),
            book_genre_names_subquery.label('book_genre_names'),

            taker_matched_ids_subquery.label('taker_matched_ids'),
            taker_matched_names_subquery.label('taker_matched_names'),

            maker_matched_ids_subquery.label('maker_matched_ids'),
            maker_matched_names_subquery.label('maker_matched_names'),

            taker_book_genre_ids_subquery.label('taker_book_genre_ids'),
            taker_book_genre_names_subquery.label('taker_book_genre_names'),
        ).join(
            Book,
            Book.id == self.model.book_id
        ).join(
            Author,
            Book.author
        ).join(
            User,
            self.model.user
        ).join(
            GenreAlias,
            Book.genres
        ).outerjoin(
            Taker,
            self.model.taker
        ).outerjoin(
            TakerBook,
            TakerBook.id == Taker.book_id
        ).outerjoin(
            TakerAuthor,
            TakerAuthor.id == TakerBook.author_id
        ).outerjoin(
            TakerUser,
            TakerUser.id == Taker.user_id
        ).outerjoin(
            TakerGenre,
            TakerBook.genres
        ).where(
            or_(
                self.model.user_id == user_id,
                Taker.user_id == user_id,
            )
        ).group_by(
            self.model.id,
            Book.id,
            Author.id,
            User.id,
            Taker.id,
            TakerBook.id,
            TakerAuthor.id,
            TakerUser.id,
        ).order_by(
            taker_match_count_subquery.desc(),
            maker_match_count_subquery.desc(),
        )

        result = (await self.session.execute(query)).one_or_none()
        if result is None:
            return None

        (
            maker,
            book,
            author,
            user,

            taker,
            taker_book,
            taker_author,
            taker_user,

            book_genre_ids,
            book_genre_names,

            taker_matched_ids,
            taker_matched_names,

            maker_matched_ids,
            maker_matched_names,

            taker_book_genre_ids,
            taker_book_genre_names,
        ) = result

        if taker is not None:
            taker_dto = TakerDTO(
                id=taker.id,
                is_received=taker.is_received,
                user=taker_user,
                book=BookResponse(
                    id=taker_book.id,
                    author=taker_author,
                    name=taker_book.name,
                    isbn=taker_book.isbn,
                    publication_year=taker_book.published_year,
                    genres=GenreDTO.build_from_lists(taker_book_genre_ids, taker_book_genre_names),
                ),
            )
        else:
            taker_dto = None

        return ExchangeResponse(
            maker=MakerDTO(
                id=maker.id,
                is_accepted=maker.is_accepted,
                is_received=maker.is_received,
                user=user,
                book=BookResponse(
                    id=book.id,
                    author=author,
                    name=book.name,
                    isbn=book.isbn,
                    publication_year=book.published_year,
                    genres=GenreDTO.build_from_lists(book_genre_ids, book_genre_names),
                ),
            ),
            taker=taker_dto,
            taker_genre_matches=GenreDTO.build_from_lists(taker_matched_ids, taker_matched_names),
            maker_genre_matches=GenreDTO.build_from_lists(maker_matched_ids, maker_matched_names),
        )

