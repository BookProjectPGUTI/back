from fastapi import HTTPException, status

EMAIL_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь с введенной почтой уже существует.'
)

USERNAME_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь с введенным псевдонимом уже существует.'
)
