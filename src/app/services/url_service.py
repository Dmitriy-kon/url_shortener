import secrets
import string

from sqlalchemy.exc import IntegrityError

from app.auth.id_provider import JwtTokenIdProvider
from app.repositories.url_repo import UrlSqlalchemyRepository
from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.abstraction.uow import UoW
from app.services.common.exception import UrlAllreadyExistsError, UserNotFoundError
from app.services.dto.dto import (
    RequestDeleteUrlDto,
    RequestInsertUrlDto,
    RequestLimitOffsetUrlDto,
    RequestUpdateUrlDto,
    ResponseUrlDto,
)


class UrlService:
    def __init__(
        self,
        url_repo: UrlSqlalchemyRepository,
        user_repo: UserSqlalchemyRepository,
        id_provider: JwtTokenIdProvider,
        uow: UoW,
    ) -> None:
        self.url_repo = url_repo
        self.uow = uow
        self.user_repo = user_repo
        self.id_provider = id_provider

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
            return None
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

        chars = string.ascii_letters + string.digits

        while True:
            short_url = "".join(secrets.choice(chars) for _ in range(20))
            if not await self.url_repo.get_url_by_short_url(short_url):
                break

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

    async def change_url(self, input_dto: RequestUpdateUrlDto) -> str:
        try:
            await self.url_repo.change_url(url_id=input_dto.urlid, url=input_dto.url)
        except IntegrityError:
            return "Some exception"
        else:
            return "Ok"

    async def delete_url(self, input_dto: RequestDeleteUrlDto) -> None:
        try:
            await self.url_repo.delete_url(url_id=input_dto.urlid)

        except Exception as ex:  # noqa: BLE001
            print(f"Some exception {ex}")  # noqa: T201
