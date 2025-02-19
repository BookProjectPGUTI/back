from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.postgres.connection import get_session_generator

get_session_depends = Annotated[
    AsyncSession,
    Depends(get_session_generator, use_cache=True)
]
