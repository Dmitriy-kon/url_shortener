from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.di.main import container_factory
from app.routes.exc_handlers.exc_handlers import init_exception_handlers
from app.routes.root import root_router


def init_di(app: FastAPI) -> None:
    setup_dishka(container_factory(), app)


def init_routes(app: FastAPI) -> None:
    app.include_router(root_router)


def create_app() -> FastAPI:
    app = FastAPI()

    init_di(app)
    init_routes(app)
    init_exception_handlers(app)
    return app
