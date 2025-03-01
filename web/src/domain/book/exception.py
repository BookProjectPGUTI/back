from fastapi import HTTPException, status

BOOK_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Книга не найден.'
)

BOOK_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Книга уже создана'
)
