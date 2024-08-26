import pytest

from app.auth.id_provider import JwtTokenIdProvider
from app.auth.jwt_processor import JwtTokenProcessor
from app.services.common.exception import UserIsNotAuthorizedError


@pytest.mark.parametrize(("user_id"), [1, 2, 3])
def test_get_current_user_id(user_id, jwt_config, system_date_time) -> None:
    token_processor = JwtTokenProcessor(jwt_config, system_date_time)
    token = token_processor.generate_token(user_id)

    jwt_token_provider_right = JwtTokenIdProvider(
        token_processor=token_processor, token=token
    )
    jwt_token_provider_wrong = JwtTokenIdProvider(
        token_processor=token_processor, token=token + "wrong"
    )
    assert jwt_token_provider_right.get_current_user_id() == user_id

    with pytest.raises(UserIsNotAuthorizedError):
        jwt_token_provider_wrong.get_current_user_id()
