from sqlalchemy.exc import IntegrityError

from app.auth.id_provider import JwtTokenIdProvider
from app.repositories.url_repo import UrlSqlalchemyRepository
from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.abstraction.uow import UoW
from app.services.common.exception import (
    UrlAllreadyExistsError,
    UrlNotFoundError,
    UserIsNotAuthorizedError,
    UserNotFoundError,
)
from app.services.dto.dto import (
    RequestDeleteUrlDto,
    RequestInsertUrlDto,
    RequestLimitOffsetUrlDto,
    RequestUpdateUrlDto,
    ResponseUrlDto,
)
from app.utils.get_short_url import GetShortUrl


class UrlService:
    def __init__(
        self,
        url_repo: UrlSqlalchemyRepository,
        user_repo: UserSqlalchemyRepository,
        id_provider: JwtTokenIdProvider,
        uow: UoW,
        get_short_url: GetShortUrl,
    ) -> None:
        self.url_repo = url_repo
        self.uow = uow
        self.user_repo = user_repo
        self.id_provider = id_provider
        self.get_short_url = get_short_url

    async def get_all_user_urls(
        self,
        input_dto: RequestLimitOffsetUrlDto,
    ) -> list[ResponseUrlDto] | None:
        user_id = self.id_provider.get_current_user_id()
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        res = await self.url_repo.get_all_user_urls(
            limit=input_dto.limit,
            offset=input_dto.offset,
            user_id=user_id,
        )
        if not res:
            return []
        return res

    async def insert_url(self, input_dto: RequestInsertUrlDto) -> ResponseUrlDto | None:
        user_id = self.id_provider.get_current_user_id()

        check_url = await self.url_repo.get_url_by_userid_and_url(
            user_id=user_id, url=input_dto.url
        )
        if check_url:
            raise UrlAllreadyExistsError(
                f"Url {input_dto.url} already exists in this user"
            )

        short_url = await self.get_short_url(self.url_repo)

        try:
            url_in_db = await self.url_repo.insert_url(
                url=input_dto.url,
                short_url=short_url,
                user_id=user_id,
            )
            await self.uow.commit()
        except IntegrityError:
            raise UrlAllreadyExistsError(
                f"Url {input_dto.url} already exists"
            ) from None
        else:
            return url_in_db

    async def generate_new_short_url(
        self, input_dto: RequestUpdateUrlDto
    ) -> ResponseUrlDto | None:
        user_id = self.id_provider.get_current_user_id()
        url_in_db = await self.url_repo.get_url_by_url_id(url_id=input_dto.urlid)
        if not url_in_db:
            raise UrlNotFoundError(f"Url with id {input_dto.urlid} not found")

        if url_in_db.user_id != user_id:
            raise UserIsNotAuthorizedError(
                f"User with id {user_id} is not authorized to update url with id\
                    {input_dto.urlid}"
            )
        new_short_url = await self.get_short_url(self.url_repo)

        try:
            url_in_db = await self.url_repo.change_url(
                url_id=input_dto.urlid, short_url=new_short_url
            )
            await self.uow.commit()
        except IntegrityError:
            return None
        else:
            return url_in_db

    async def delete_url(self, input_dto: RequestDeleteUrlDto) -> ResponseUrlDto | None:
        user_id = self.id_provider.get_current_user_id()
        url_in_db = await self.url_repo.get_url_by_url_id(url_id=input_dto.urlid)
        if not url_in_db:
            raise UrlNotFoundError(f"Url with id {input_dto.urlid} not found")

        if url_in_db.user_id != user_id:
            raise UserIsNotAuthorizedError(
                f"User with id {user_id} is not authorized to delete url with id\
                    {input_dto.urlid}"
            )
        try:
            url = await self.url_repo.delete_url(url_id=input_dto.urlid)
            await self.uow.commit()
        except Exception as ex:  # noqa: BLE001
            print(f"Some exception {ex}")  # noqa: T201
            return None
        else:
            return url
