from app.auth.jwt_processor import JwtTokenProcessor
from app.services.common.exception import UserIsNotAuthorizedError


class JwtTokenIdProvider:
    def __init__(self, token_processor: JwtTokenProcessor, token: str) -> None:
        self.token_processor = token_processor
        self.token = token

    def get_current_user_id(self) -> int:
        user_id = self.token_processor.validate_token(self.token)
        if not user_id:
            raise UserIsNotAuthorizedError("Неверные данные для авторизации")

        return user_id
