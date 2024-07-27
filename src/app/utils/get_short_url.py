import secrets

from app.main.config import UrlConfig
from app.repositories.url_repo import UrlSqlalchemyRepository


class GetShortUrl:
    def __init__(self, config: UrlConfig) -> None:
        self.config = config

    async def __call__(self, url_repo: UrlSqlalchemyRepository) -> str:
        protocol = self.config.protocol
        host = self.config.host

        while True:
            short_code = secrets.token_urlsafe(16)
            stort_url = f"{protocol}://{host}/?short={short_code}"
            if not await url_repo.get_url_by_short_url(short_url=stort_url):
                break
        return stort_url
