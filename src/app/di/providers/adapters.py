from collections.abc import AsyncIterable

from dishka import Provider, Scope, alias, from_context, provide
from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.auth.id_provider import JwtTokenIdProvider
from app.auth.jwt_processor import JwtTokenProcessor
from app.main.config import Config
from app.repositories.url_repo import UrlSqlalchemyRepository
from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.abstraction.uow import UoW
from app.utils.datetime_provide import SystemDateTime, Timezone
from app.utils.get_short_url import GenerateShortUrl, GenerateShortUrls, GetShortUrl


class SqlalchemyProvider(Provider):
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
        UrlSqlalchemyRepository, scope=Scope.REQUEST, provides=UrlSqlalchemyRepository
    )


class UrlsProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_config(self) -> Config:
        return Config()

    @provide(scope=Scope.REQUEST)
    def provide_get_short_url(self, config: Config) -> GetShortUrl:
        return GetShortUrl(config.url_config)

    @provide(scope=Scope.REQUEST)
    def generate_short_url(self, config: Config) -> GenerateShortUrl:
        return GenerateShortUrl(config.url_config)
    @provide(scope=Scope.REQUEST)
    def generate_short_urls(self, config: Config) -> GenerateShortUrls:
        return GenerateShortUrls(config.url_config)


class AuthProvider(Provider):
    request = from_context(scope=Scope.REQUEST, provides=Request)

    @provide(scope=Scope.APP)
    def provide_config(self) -> Config:
        return Config()

    @provide(scope=Scope.APP)
    def provide_system_datetime(self) -> SystemDateTime:
        return SystemDateTime(Timezone.UTC)

    @provide(scope=Scope.APP)
    def provide_jwt_token_processor(
        self, config: Config, system_datetime: SystemDateTime
    ) -> JwtTokenProcessor:
        return JwtTokenProcessor(config.jwt_config, system_datetime)

    @provide(scope=Scope.REQUEST, provides=JwtTokenIdProvider)
    def id_provider(
        self, token_processor: JwtTokenProcessor, request: Request
    ) -> JwtTokenIdProvider:
        return JwtTokenIdProvider(token_processor=token_processor, token=request.auth)
