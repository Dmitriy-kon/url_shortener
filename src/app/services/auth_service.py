from sqlalchemy.exc import IntegrityError

from app.auth.hasher import hash_password, verify_password
from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.abstraction.uow import UoW
from app.services.common.exception import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserPasswordNotMatchError,
)
from app.services.dto.dto import (
    RequestUserDto,
    ResponseUserDto,
)


class AuthService:
    def __init__(self, user_repo: UserSqlalchemyRepository, uow: UoW) -> None:
        self.user_repo = user_repo
        self.uow = uow

    async def register(self, input_dto: RequestUserDto) -> str:
        hashed_password = hash_password(input_dto.password)
        try:
            await self.user_repo.create_user(input_dto.username, hashed_password)
            await self.uow.commit()
        except IntegrityError:
            raise UserAlreadyExistsError(
                f"User with username {input_dto.username} already exist"
            ) from None
        else:
            return "Ok"

    async def login(self, input_dto: RequestUserDto) -> ResponseUserDto:
        user_dto = await self.user_repo.get_user_by_username(input_dto.username)
        if not user_dto:
            raise UserNotFoundError(
                f"User with username {input_dto.username} does not exist"
            )
        if not verify_password(input_dto.password, user_dto.hashed_password):
            raise UserPasswordNotMatchError(
                f"Incorrect password for user {input_dto.username}"
            )
        return user_dto
