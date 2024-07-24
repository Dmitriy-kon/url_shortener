from collections.abc import AsyncIterable

from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.main.config import Config
from app.repositories.url_repo import SqlalchemyUrlRepository
from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.abstraction.uow import UoW


class SqlalchemtProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_config(self) -> Config:
        return Config()

    @provide(scope=Scope.APP)
    def provide_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.db_config.db_uri, echo=True)

    @provide(scope=Scope.APP)
    def provide_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    uow = alias(source=AsyncSession, provides=UoW)

    user_repository = provide(
        UserSqlalchemyRepository, scope=Scope.REQUEST, provides=UserSqlalchemyRepository
    )
    url_repository = provide(
        SqlalchemyUrlRepository, scope=Scope.REQUEST, provides=SqlalchemyUrlRepository
    )
