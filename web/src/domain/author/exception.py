from fastapi import HTTPException, status

AUTHOR_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Автор не найден'
)
