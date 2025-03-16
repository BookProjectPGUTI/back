from typing import List
from uuid import UUID

from sqlalchemy import select, func, ScalarSelect, or_, FunctionFilter
from sqlalchemy.orm import aliased, InstrumentedAttribute

from src.api.book.dto import BookResponse
from src.api.exchange.dto import ExchangeResponse
from src.domain.taker.dto import TakerDTO
from src.domain.maker.dto import MakerDTO, MakerMatchDTO
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
                genre_alias.id.in_(genre_query)
            )

        genre_alias = aliased(Genre)

        maker_genre_subquery = select(
            BookGenre.genre_id
        ).where(
            BookGenre.book_id == self.model.book_id
        ).scalar_subquery()

        book_genre_ids_subquery = _build_array_query(genre_alias.id, maker_genre_subquery)
        book_genre_names_subquery = _build_array_query(genre_alias.name, maker_genre_subquery)

        taker_matches_subquery = select(
            WishList.genre_id
        ).where(
            WishList.user_id == user_id
        ).scalar_subquery()

        taker_match_count_subquery = func.count(
            genre_alias.id
        ).filter(
            genre_alias.id.in_(taker_matches_subquery)
        )

        taker_matched_ids_subquery = _build_array_query(genre_alias.id, taker_matches_subquery)
        taker_matched_names_subquery = _build_array_query(genre_alias.name, taker_matches_subquery)

        maker_matches_subquery = select(
            WishList.genre_id
        ).where(
            WishList.user_id == self.model.user_id
        ).scalar_subquery()

        maker_match_count_subquery = func.count(
            genre_alias.id
        ).filter(
            genre_alias.id.in_(maker_matches_subquery)
        )

        maker_matched_ids_subquery = _build_array_query(genre_alias.id, maker_matches_subquery)
        maker_matched_names_subquery = _build_array_query(genre_alias.name, maker_matches_subquery)

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
            genre_alias,
            Book.genres
        ).outerjoin(
            Taker,
            self.model.taker
        ).where(
            self.model.is_accepted.is_(False),
            self.model.is_received.is_(False),
            self.model.user_id != user_id,
            Taker.id.is_(None),
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
        genre_alias = aliased(Genre)
        book_genre_alias = aliased(BookGenre)
        taker_book_genre_alias = aliased(BookGenre)
        taker_genre_alias = aliased(Genre)
        taker_book_alias = aliased(Book)
        taker_author_alias = aliased(Author)
        taker_user_alias = aliased(User)

        taker_matches_subquery = select(
            WishList.user_id,
            func.array_agg(WishList.genre_id).label('taker_matched_ids'),
            func.array_agg(genre_alias.name).label('taker_matched_names')
        ).join(
            genre_alias, genre_alias.id == WishList.genre_id
        ).group_by(
            WishList.user_id
        ).subquery()

        maker_matches_subquery = select(
            WishList.user_id,
            func.array_agg(WishList.genre_id).label('maker_matched_ids'),
            func.array_agg(genre_alias.name).label('maker_matched_names')
        ).join(
            genre_alias, genre_alias.id == WishList.genre_id
        ).group_by(
            WishList.user_id
        ).subquery()

        book_genre_subquery = select(
            book_genre_alias.book_id,
            func.array_agg(genre_alias.id).label('book_genre_ids'),
            func.array_agg(genre_alias.name).label('book_genre_names')
        ).join(
            genre_alias, genre_alias.id == book_genre_alias.genre_id
        ).group_by(
            book_genre_alias.book_id
        ).subquery()

        taker_book_genre_subquery = select(
            taker_book_genre_alias.book_id,
            func.array_agg(taker_genre_alias.id).label('taker_book_genre_ids'),
            func.array_agg(taker_genre_alias.name).label('taker_book_genre_names')
        ).join(
            taker_genre_alias, taker_genre_alias.id == taker_book_genre_alias.genre_id
        ).group_by(
            taker_book_genre_alias.book_id
        ).subquery()

        taker_match_count_subquery = select(
            func.count(WishList.genre_id).label('taker_match_count')
        ).where(
            WishList.user_id == Taker.user_id
        ).correlate(Taker).scalar_subquery()

        maker_match_count_subquery = select(
            func.count(WishList.genre_id).label('maker_match_count')
        ).where(
            WishList.user_id == self.model.user_id
        ).correlate(self.model).scalar_subquery()

        query = select(
            self.model,
            Book,
            Author,
            User,
            Taker,
            taker_book_alias,
            taker_author_alias,
            taker_user_alias,
            book_genre_subquery.c.book_genre_ids,
            book_genre_subquery.c.book_genre_names,
            taker_matches_subquery.c.taker_matched_ids,
            taker_matches_subquery.c.taker_matched_names,
            maker_matches_subquery.c.maker_matched_ids,
            maker_matches_subquery.c.maker_matched_names,
            taker_book_genre_subquery.c.taker_book_genre_ids,
            taker_book_genre_subquery.c.taker_book_genre_names
        ).join(
            Book, Book.id == self.model.book_id
        ).join(
            Author, Book.author_id == Author.id
        ).join(
            User, self.model.user_id == User.id
        ).outerjoin(
            Taker, self.model.id == Taker.id
        ).outerjoin(
            taker_book_alias, Taker.book_id == taker_book_alias.id
        ).outerjoin(
            taker_author_alias, taker_book_alias.author_id == taker_author_alias.id
        ).outerjoin(
            taker_user_alias, Taker.user_id == taker_user_alias.id
        ).outerjoin(
            book_genre_subquery, book_genre_subquery.c.book_id == Book.id
        ).outerjoin(
            taker_matches_subquery, taker_matches_subquery.c.user_id == Taker.user_id
        ).outerjoin(
            maker_matches_subquery, maker_matches_subquery.c.user_id == self.model.user_id
        ).outerjoin(
            taker_book_genre_subquery, taker_book_genre_subquery.c.book_id == Taker.book_id
        ).where(
            or_(
                self.model.user_id == user_id,
                Taker.user_id == user_id,
            )
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

