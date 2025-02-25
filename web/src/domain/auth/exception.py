from fastapi import HTTPException
from starlette import status

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверные данные для входа.'
)

ACCESS_NOT_FOUND = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Access токен не найден.'
)

ACCESS_EXPIRES = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Access токен закончил своё действие.'
)

REFRESH_NOT_FOUND = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Refresh токен не найден.'
)

REFRESH_EXPIRES = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Refresh токен закончил своё действие.'
)
