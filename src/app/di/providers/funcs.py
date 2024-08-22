from functools import partial

from dishka import Provider, Scope, provide

from app.main.config import Config
from app.utils.get_short_url import (
    generate_short_url,
    generate_short_urls,
)


class UrlsFunctionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_config(self) -> Config:
        return Config()

    @provide(scope=Scope.REQUEST)
    def provide_generate_short_urls(self, config: Config) -> generate_short_url:
        return partial(generate_short_url, config.url_config)

    @provide(scope=Scope.REQUEST)
    def generate_short_url(self, config: Config) -> generate_short_urls:
        return partial(generate_short_urls, config.url_config)
