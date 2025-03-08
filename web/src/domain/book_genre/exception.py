from fastapi import HTTPException, status

BOOK_GENRE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Жанры книги не найдены'
)