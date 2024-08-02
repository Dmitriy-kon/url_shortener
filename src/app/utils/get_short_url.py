import secrets

from app.main.config import UrlConfig
from app.repositories.url_repo import UrlSqlalchemyRepository
from app.services.dto.dto import ResponseUrlDto


class GetShortUrl:
    def __init__(self, config: UrlConfig) -> None:
        self.config = config

    async def __call__(self, url_repo: UrlSqlalchemyRepository) -> str:
        while True:
            short_code = secrets.token_urlsafe(16)
            short_url = short_code
            if not await url_repo.get_url_by_short_url(short_url=short_url):
                break
        return short_url


class GenerateShortUrls:
    def __init__(self, config: UrlConfig) -> None:
        self.config = config

    async def __call__(self, urls_dto: list[ResponseUrlDto]) -> list[ResponseUrlDto]:
        res = []
        for i in urls_dto:
            i.short_url = (
                f"{self.config.protocol}://{self.config.host}/t/?short={i.short_url}"
            )
            res.append(i)

        return res


class GenerateShortUrl:
    def __init__(self, config: UrlConfig) -> None:
        self.config = config

    async def __call__(self, url_dto: ResponseUrlDto) -> ResponseUrlDto | None:
        url_dto.short_url = (
            f"{self.config.protocol}://{self.config.host}/t/?short={url_dto.short_url}"
        )
        return url_dto
