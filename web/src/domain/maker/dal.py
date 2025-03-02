from typing import List
from uuid import UUID

from sqlalchemy import select, func, Select, ScalarSelect
from sqlalchemy.orm import aliased

from src.api.book.dto import BookResponse
from src.api.exchange.dto import MakerDTO
from src.domain.abc.dal import ABCDAL
from src.domain.author.model import Author
from src.domain.book.model import Book
from src.domain.book_genre.model import BookGenre
from src.domain.genre.dto import GenreDTO
from src.domain.genre.model import Genre
from src.domain.maker.model import Maker
from src.domain.user.model import User
from src.domain.wish_list.model import WishList


class MakerDAL(ABCDAL[Maker]):
    async def get_matched_makers(self, user_id: UUID) -> List[MakerDTO]:
        def _build_array_query(field, genre_query: ScalarSelect) -> Select:
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
            MakerDTO(
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
