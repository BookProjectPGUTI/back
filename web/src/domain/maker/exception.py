from fastapi import HTTPException, status

MAKER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже начал поиск пары для обмена.'
)

MAKER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Мейкер не найден'
)

MAKER_ALREADY_TAKEN = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Мейкер уже занят.'
)

MAKER_ALREADY_ACCEPTED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Мейкер уже принял обмен.'
)

MAKER_ALREADY_RECEIVED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Мейкер уже подтвердил получение.'
)

MAKER_NOT_ACCEPTED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Мейкер ещё не подтвердил обмен'
)

MAKER_WITHOUT_TRACK_NUMBER = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Мейкер ещё не ввел трек-номер'
)
