from sqlalchemy.exc import IntegrityError

from app.auth.hasher import hash_password, verify_password
from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.common.exception import UserNotFoundError
from app.services.dto.dto import RequestUidDto, RequestUserDto, ResponseUserDto


class AuthService:
    def __init__(self, user_repo: UserSqlalchemyRepository) -> None:
        self.user_repo = user_repo

    async def get_user_by_username(self, input_dto: RequestUserDto) -> ResponseUserDto:
        user = await self.user_repo.get_user_by_username(input_dto.username)
        if not user:
            raise UserNotFoundError(
                f"User with username {input_dto.username} does not exist"
            )
        return user

    async def get_user_by_id(self, input_dto: RequestUidDto) -> ResponseUserDto:
        user = await self.user_repo.get_user_by_id(input_dto.id)
        if not user:
            raise UserNotFoundError(f"User with id {input_dto.id} does not exist")
        return user

    async def create_user(self, input_dto: RequestUserDto) -> str:
        hashed_password = hash_password(input_dto.password)
        try:
            await self.user_repo.create_user(input_dto.username, hashed_password)
        except IntegrityError:
            return "Some exception"
        else:
            return "Ok"
