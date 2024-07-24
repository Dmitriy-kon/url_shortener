from sqlalchemy.exc import IntegrityError

from app.repositories.url_repo import SqlalchemyUrlRepository
from app.services.dto.dto import (
    RequestDeleteUrlDto,
    RequestInsertUrlDto,
    RequestLimitOffsetUrlDto,
    RequestUpdateUrlDto,
    ResponseUrlDto,
)


class UrlService:
    def __init__(self, url_repo: SqlalchemyUrlRepository) -> None:
        self.url_repo = url_repo

    async def get_all_user_urls(
        self, input_dto: RequestLimitOffsetUrlDto
    ) -> list[ResponseUrlDto] | None:
        res = await self.url_repo.get_all_user_urls(
            limit=input_dto.limit, offset=input_dto.offset, user_id=input_dto.user_id
        )
        if not res:
            return None
        return res

    async def insert_url(self, input_dto: RequestInsertUrlDto) -> str:
        try:
            await self.url_repo.insert_url(
                url=input_dto.url,
                short_url=input_dto.short_url,
                user_id=input_dto.user_id,
            )
        except IntegrityError:
            return "Some exception"
        else:
            return "Ok"

    async def change_url(self, input_dto: RequestUpdateUrlDto) -> str:
        try:
            await self.url_repo.change_url(
                url_id=input_dto.urlid, url=input_dto.url, short_url=input_dto.short_url
            )
        except IntegrityError:
            return "Some exception"
        else:
            return "Ok"

    async def delete_url(self, input_dto: RequestDeleteUrlDto) -> None:
        try:
            await self.url_repo.delete_url(url_id=input_dto.urlid)

        except Exception as ex:  # noqa: BLE001
            print(f"Some exception {ex}") # noqa: T201
