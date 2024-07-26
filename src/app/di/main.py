from dishka import AsyncContainer, make_async_container

from app.di.providers.adapters import AuthProvider, SqlalchemyProvider
from app.di.providers.services import ServiceProvider


def container_factory() -> AsyncContainer:
    return make_async_container(
        ServiceProvider(),
        SqlalchemyProvider(),
        AuthProvider()
    )
