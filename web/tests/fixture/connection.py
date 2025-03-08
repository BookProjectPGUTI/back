from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.postgres.connection import async_session_maker


@pytest_asyncio.fixture()
async def session() -> AsyncGenerator[AsyncSession, None]:
    session_ = async_session_maker()
    try:
        yield session_
    except Exception as exc:
        raise exc
    finally:
        await session_.rollback()
        await session_.close()
        