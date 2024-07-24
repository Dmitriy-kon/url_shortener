from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.models import UrlDb
from app.services.dto.dto import ResponseUrlDto


class SqlalchemyUrlRepository:
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

    async def insert_url(self, url: str, short_url: str, user_id: int) -> None:
        stmt = insert(UrlDb).values(url=url, short_url=short_url, user_id=user_id)
        await self.session.execute(stmt)

    async def change_url(self, url_id: int, url: str, short_url: str) -> None:
        stmt = (
            update(UrlDb)
            .where(UrlDb.urlid == url_id)
            .values(url=url, short_url=short_url)
        )
        await self.session.execute(stmt)

    async def delete_url(self, url_id: int) -> None:
        stmt = delete(UrlDb).where(UrlDb.urlid == url_id)
        await self.session.execute(stmt)
