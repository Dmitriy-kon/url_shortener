from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.repositories.models import UserDb
from app.services.dto.dto import ResponseUserDto


class UserSqlalchemyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str) -> ResponseUserDto | None:
        stmt = (
            select(UserDb)
            .options(selectinload(UserDb.us_urls))
            .where(UserDb.username == username)
        )
        user_result = await self.session.execute(stmt)
        user = user_result.unique().scalar()
        if not user:
            return None
        return user.to_dto()

    async def get_user_by_id(self, user_id: int) -> ResponseUserDto | None:
        stmt = (
            select(UserDb)
            .options(selectinload(UserDb.us_urls))
            .where(UserDb.uid == user_id)
        )
        user_result = await self.session.execute(stmt)
        user = user_result.unique().scalar()
        if not user:
            return None
        return user.to_dto()

    async def create_user(
        self, username: str, hashed_password: str
    ) -> ResponseUserDto | None:
        stmt = (
            insert(UserDb)
            .values(username=username, hashed_password=hashed_password)
            .options(selectinload(UserDb.us_urls))
            .returning(UserDb)
        )
        user_in_db = await self.session.execute(stmt)
        user = user_in_db.unique().scalar()
        if not user:
            return None
        return user.to_dto()

    async def change_user(
        self, user_id: int, username: str, hashed_password: str
    ) -> ResponseUserDto | None:
        stmt = (
            update(UserDb)
            .where(UserDb.uid == user_id)
            .values(username=username, hashed_password=hashed_password)
            .options(selectinload(UserDb.us_urls))
            .returning(UserDb)
        )
        user_in_db = await self.session.execute(stmt)
        user = user_in_db.unique().scalar()
        if not user:
            return None
        return user.to_dto()

    async def delete_user(self, user_id: int) -> None | str:
        stmt = delete(UserDb).where(UserDb.uid == user_id).returning(UserDb)
        res = await self.session.execute(stmt)
        if res.scalar() is None:
            return None
        return "User deleted"
