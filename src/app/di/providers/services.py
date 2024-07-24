from dishka import Provider, Scope, provide

from app.services.auth_service import AuthService
from app.services.url_service import UrlService


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    auth_service = provide(AuthService)
    url_service = provide(UrlService)
