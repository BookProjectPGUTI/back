from fastapi import HTTPException, status

USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Пользователь не найден.'
)

EMAIL_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь с введенной почтой уже существует.'
)

USERNAME_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь с введенным псевдонимом уже существует.'
)

USER_ALREADY_CONFIRMED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже подтвердил почту.'
)

USER_DISABLED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Пользователь заблокирован.'
)

USER_UNCONFIRMED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Почта пользователя не подтверждена.'
)

USER_NOT_NAMED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Пользователь не ввел ФИО'
)
