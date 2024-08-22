from sqlalchemy.exc import IntegrityError

from app.repositories.abstract import UrlRepository
from app.services.abstraction.uow import UoW
from app.services.common.exception import (
    UrlNotFoundError,
)
from app.services.dto.dto import (
    ResponseUrlDto,
)


class GetUrlFromShortUrl:
    def __init__(self, url_repo: UrlRepository, uow: UoW) -> None:
        self.url_repo = url_repo
        self.uow = uow

    async def __call__(self, short_url: str) -> ResponseUrlDto | None:
        # short_url =
        url = await self.url_repo.get_url_by_short_url(short_url=short_url)
        if not url:
            return None
        try:
            await self.url_repo.update_url_clicks(url_id=url.urlid)
            await self.uow.commit()
        except IntegrityError as exc:
            raise UrlNotFoundError(f"Url with short url {short_url} not found") from exc

        if not url:
            return None
        return url
