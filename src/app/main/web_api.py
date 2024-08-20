from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.di.main import container_factory
from app.routes.exc_handlers.exc_handlers import init_exception_handlers
from app.routes.root import root_router


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def init_static(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory="src/app/static"), name="static")

def init_di(app: FastAPI) -> None:
    setup_dishka(container_factory(), app)


def init_routes(app: FastAPI) -> None:
    app.include_router(root_router)


def create_app() -> FastAPI:
    app = FastAPI()

    init_cors(app)
    init_static(app)
    init_di(app)
    init_routes(app)
    init_exception_handlers(app)
    return app
