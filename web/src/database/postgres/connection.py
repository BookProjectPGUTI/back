from functools import wraps
from typing import Awaitable, Callable, TypeVar, ParamSpec, AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config.postgres import POSTGRES_CONFIG

async_engine = create_async_engine(
    POSTGRES_CONFIG.connection_url(),
    echo=False,
    future=True,
    poolclass=NullPool
)
async_session_maker = async_sessionmaker(async_engine, class_=AsyncSession)


async def get_session_generator() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_maker()
    try:
        async with session.begin():
            yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


T = TypeVar("T")
P = ParamSpec("P")


def session_decorator(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    @wraps(fn)
    async def decorated(*args: P.args, **kwargs: P.kwargs) -> T:
        is_session_in_args = any(isinstance(arg, AsyncSession) for arg in args)
        is_session_in_kwargs = any(isinstance(v, AsyncSession) for _, v in kwargs.items())
        if is_session_in_args or is_session_in_kwargs:
            return await fn(*args, **kwargs)
        session = async_session_maker()
        try:
            async with session.begin():
                kwargs['session'] = session
                result = await fn(*args, **kwargs)
            await session.commit()
            return result
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    return decorated
