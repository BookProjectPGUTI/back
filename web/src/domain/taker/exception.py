from fastapi import HTTPException, status

TAKER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже выбрал пару для обмена.'
)
