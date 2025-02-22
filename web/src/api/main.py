from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from src.api.auth.router import auth_router_v1
from src.config.web import WEB_CONFIG
from src.config.mail import MAIL_CONFIG
from src.utils.router_utils import include_routers


@asynccontextmanager
async def lifespan(app_: FastAPI):
    from src.api.default.router import default_router_v1

    routers_v1 = [
        auth_router_v1
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
    debug=WEB_CONFIG.debug,
    lifespan=lifespan,
    root_path='/api'
)
