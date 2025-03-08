from fastapi import HTTPException, status

MAKER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже начал поиск пары для обмена.'
)

MAKER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Мейкер не найден'
)
