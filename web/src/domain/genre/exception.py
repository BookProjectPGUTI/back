from fastapi import HTTPException, status

GENRE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Жанр не найден.'
)
