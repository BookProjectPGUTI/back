from typing import Annotated

from fastapi import Depends

from src.domain.auth.dto import AccessTokenDTO
from src.domain.auth.service import UserFilter

user_depends = Annotated[
    AccessTokenDTO, Depends(UserFilter())
]
