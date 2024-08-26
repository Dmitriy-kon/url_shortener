from unittest.mock import Mock

from sqlalchemy.exc import IntegrityError

from app.repositories.abstract import UserRepository
from app.services.dto.dto import ResponseUserDto

data_users: list[ResponseUserDto] = []


class MockUserRepository(UserRepository):
    async def get_user_by_username(self, username: str) -> ResponseUserDto | None:
        for user in data_users:
            if user.username == username:
                return user
        return None

    async def get_user_by_id(self, user_id: int) -> ResponseUserDto | None:
        for user in data_users:
            if user.uid == user_id:
                return user
        return None

    async def create_user(self, username: str, hashed_password: str) -> ResponseUserDto:
        uid_in_db = max([i.uid for i in data_users]) + 1 if data_users else 1
        if username in [i.username for i in data_users]:
            raise IntegrityError(Mock(), Mock(), Mock())

        user_in_db = ResponseUserDto(
            uid=uid_in_db,
            username=username,
            hashed_password=hashed_password,
            urls=None,
        )
        data_users.append(user_in_db)
        return user_in_db

    async def change_user(
        self, user_id: int, username: str, hashed_password: str
    ) -> ResponseUserDto | None:
        for user in data_users:
            if user.uid == user_id:
                user.username = username
                user.hashed_password = hashed_password
                return user
        return None

    async def delete_user(self, user_id: int) -> ResponseUserDto | None:
        for user in data_users:
            if user.uid == user_id:
                data_users.remove(user)
                return user
        return None
