from fastapi import HTTPException
from starlette import status

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверные данные для входа.'
)
