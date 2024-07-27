from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.models import UrlDb
from app.services.dto.dto import ResponseUrlDto


class UrlSqlalchemyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_user_urls(
        self, user_id: int, limit: int, offset: int
    ) -> list[ResponseUrlDto] | None:
        stmt = select(UrlDb).where(UrlDb.user_id == user_id).limit(limit).offset(offset)
        url_results = await self.session.execute(stmt)
        urls = url_results.scalars()
        if not urls:
            return None
        return [url.to_dto() for url in urls]

    async def get_url_by_short_url(self, short_url: str) -> ResponseUrlDto | None:
        stmt = select(UrlDb).where(UrlDb.short_url == short_url)
        url_result = await self.session.execute(stmt)
        url = url_result.scalar()
        if not url:
            return None
        return url.to_dto()

    async def get_url_by_userid_and_url(
        self, user_id: int, url: str
    ) -> ResponseUrlDto | None:
        stmt = select(UrlDb).where(UrlDb.user_id == user_id, UrlDb.url == url)
        url_result = await self.session.execute(stmt)
        res_url = url_result.scalar()
        if not res_url:
            return None
        return res_url.to_dto()

    async def get_url_by_url_id(self, url_id: int) -> ResponseUrlDto | None:
        stmt = select(UrlDb).where(UrlDb.urlid == url_id)
        url_result = await self.session.execute(stmt)
        res_url = url_result.scalar()
        if not res_url:
            return None
        return res_url.to_dto()

    async def insert_url(
        self, url: str, short_url: str, user_id: int
    ) -> ResponseUrlDto | None:
        stmt = (
            insert(UrlDb)
            .values(url=url, short_url=short_url, user_id=user_id)
            .returning(UrlDb)
        )
        res = await self.session.execute(stmt)
        url_in_db = res.scalar()
        if not url_in_db:
            return None
        return url_in_db.to_dto()

    async def change_url(self, url_id: int, short_url: str) -> ResponseUrlDto | None:
        stmt = (
            update(UrlDb)
            .where(UrlDb.urlid == url_id)
            .values(short_url=short_url)
            .returning(UrlDb)
        )
        res = await self.session.execute(stmt)
        url_in_db = res.scalar()
        if not url_in_db:
            return None
        return url_in_db.to_dto()

    async def delete_url(self, url_id: int) -> None:
        stmt = delete(UrlDb).where(UrlDb.urlid == url_id)
        await self.session.execute(stmt)
