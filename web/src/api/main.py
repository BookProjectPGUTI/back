from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from src.config.web import WEB_CONFIG


@asynccontextmanager
async def lifespan(app_: FastAPI):
    from src.api.default.router import default_router_v1

    app_.include_router(default_router_v1)

    yield


app = FastAPI(
    title='Book Project APi',
    debug=WEB_CONFIG.debug,
    lifespan=lifespan,
    redirect_slashes=True,
)
