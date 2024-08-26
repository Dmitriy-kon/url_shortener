import pytest

from app.auth.id_provider import JwtTokenIdProvider
from app.auth.jwt_processor import JwtTokenProcessor


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_current_user_id(user_id, jwt_config, system_date_time) -> None:
    token_processor = JwtTokenProcessor(jwt_config, system_date_time)
    token = token_processor.generate_token(user_id)

    jwt_token_provider = JwtTokenIdProvider(
        token_processor=token_processor, token=token
    )
    assert jwt_token_provider.get_current_user_id() == user_id
