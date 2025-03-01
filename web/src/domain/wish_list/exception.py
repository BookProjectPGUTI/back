from fastapi import HTTPException, status

WISH_LIST_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Список желаемых жанров не найден'
)
