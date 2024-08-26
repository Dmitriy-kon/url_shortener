import pytest

from app.auth.jwt_processor import JwtTokenProcessor


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_generate_token(user_id, jwt_config, system_date_time) -> None:
    jwt_token_processor = JwtTokenProcessor(jwt_config, system_date_time)

    token = jwt_token_processor.generate_token(user_id)
    assert token is not None
    assert isinstance(token, str)


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_validate_token(user_id, jwt_config, system_date_time) -> None:
    jwt_token_processor = JwtTokenProcessor(jwt_config, system_date_time)
    token_right = jwt_token_processor.generate_token(user_id)
    token_wrong = token_right + "wrong"

    user_id_from_wrong_token = jwt_token_processor.validate_token(token_wrong)
    user_id_from_token = jwt_token_processor.validate_token(token_right)
    assert user_id_from_token == user_id
    assert user_id_from_wrong_token is None
