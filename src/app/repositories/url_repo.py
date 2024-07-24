from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.models import UrlDb


class SqlalchemyUrlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_user_urls(self, user_id: int):
        stmt = select(UrlDb).where(UrlDb.user_id == user_id)
        url_results = await self.session.execute(stmt)
        urls = url_results.scalars()
        if not urls:
            return []
        return urls

    async def insert_url(self, url: UrlDb):
        stmt = insert(UrlDb).values(url)
        await self.session.execute(stmt)

    async def delete_url(self, url_id: int):
        stmt = delete(UrlDb).where(UrlDb.id == url_id)
        await self.session.execute(stmt)
