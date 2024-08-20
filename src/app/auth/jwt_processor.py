from datetime import timedelta

from jwt import PyJWTError, decode, encode

from app.main.config import JwtConfig
from app.utils.datetime_provide import SystemDateTime


class JwtTokenProcessor:
    def __init__(
        self, jwt_config: JwtConfig, datetime_provider: SystemDateTime
    ) -> None:
        self.jwt_config = jwt_config
        self.datetime_provider = datetime_provider

    def generate_token(self, user_id: int) -> str:
        issued_at = self.datetime_provider.get_current_time()
        expiration = issued_at + timedelta(days=self.jwt_config.expire)

        payload = {"iat": issued_at, "exp": expiration, "sub": str(user_id)}
        return encode(
            payload, self.jwt_config.secret_key, algorithm=self.jwt_config.algorithm
        )

    def validate_token(self, token: str) -> int | None:
        try:
            payload = decode(
                token,
                self.jwt_config.secret_key,
                algorithms=[self.jwt_config.algorithm],
            )
            return int(payload["sub"])
        except (PyJWTError, KeyError):
            return None
