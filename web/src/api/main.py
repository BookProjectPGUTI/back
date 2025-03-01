from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from src.api.auth.router import auth_router_v1
from src.config.web import WEB_CONFIG
from src.config.mail import MAIL_CONFIG  # noqa
from src.utils.router_utils import include_routers
from src.database.postgres.models import *  # noqa


@asynccontextmanager
async def lifespan(app_: FastAPI):
    from src.api.default.router import default_router_v1
    from src.api.user.router import users_router_v1
    from src.api.genre.router import genres_router_v1
    from src.api.book.router import books_router_v1
    routers_v1 = [
        auth_router_v1,
        users_router_v1,
        genres_router_v1,
        books_router_v1,
    ]

    root_router_v1 = include_routers(APIRouter(prefix='/v1'), routers_v1)

    main_router = include_routers(
        default_router_v1,
        (
            root_router_v1,
        )
    )
    app_.include_router(main_router)

    yield


app = FastAPI(
    title='Book Project API',
    summary='Сервис по обмену книгами между пользователями.',
    version='0.2',
    debug=WEB_CONFIG.debug,
    lifespan=lifespan,
    root_path='/api',
)

origins = [
    "http://4300193-op40148.twc1.net",
    "https://4300193-op40148.twc1.net",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
