from fastapi import HTTPException, status

EXCHANGE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Вы ещё не участвуете ни в одном обмене'
)
