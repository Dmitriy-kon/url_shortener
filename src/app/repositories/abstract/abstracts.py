from typing import Protocol, runtime_checkable

from app.services.dto.dto import ResponseUrlDto, ResponseUserDto


@runtime_checkable
class UrlRepository(Protocol):
    async def get_all_user_urls(
        self, user_id: int, limit: int, offset: int
    ) -> list[ResponseUrlDto] | None:
        raise NotImplementedError

    async def get_url_by_short_url(self, short_url: str) -> ResponseUrlDto | None:
        raise NotImplementedError

    async def get_url_by_userid_and_url(
        self, user_id: int, url: str
    ) -> ResponseUrlDto | None:
        raise NotImplementedError

    async def get_url_by_url_id(self, url_id: int) -> ResponseUrlDto | None:
        raise NotImplementedError

    async def insert_url(
        self, url: str, short_url: str, user_id: int
    ) -> ResponseUrlDto | None:
        raise NotImplementedError

    async def change_url(self, url_id: int, short_url: str) -> ResponseUrlDto | None:
        raise NotImplementedError

    async def update_url_clicks(self, url_id: int) -> ResponseUrlDto | None:
        raise NotImplementedError

    async def delete_url(self, url_id: int) -> ResponseUrlDto | None:
        raise NotImplementedError


@runtime_checkable
class UserRepository(Protocol):
    async def get_user_by_id(self, user_id: int) -> ResponseUserDto | None:
        raise NotImplementedError

    async def get_user_by_username(self, username: str) -> ResponseUserDto | None:
        raise NotImplementedError

    async def create_user(
        self, username: str, hashed_password: str
    ) -> ResponseUserDto | None:
        raise NotImplementedError

    async def change_user(
        self, user_id: int, username: str, hashed_password: str
    ) -> ResponseUserDto | None:
        raise NotImplementedError

    async def delete_user(self, user_id: int) -> ResponseUserDto | None:
        raise NotImplementedError
