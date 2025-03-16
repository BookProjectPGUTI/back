from fastapi import HTTPException, status

TAKER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже выбрал пару для обмена.'
)

TAKER_ALREADY_RECEIVED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Тейкер уже подтвердил получение.'
)

TAKER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Тейкер не найден.'
)
