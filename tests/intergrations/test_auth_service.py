from contextlib import nullcontext as not_raise

import pytest

from app.services.auth_service import AuthService
from app.services.common.exception import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserPasswordNotMatchError,
)
from app.services.dto.dto import RequestUserDto, ResponseUserDto
from tests.mocks.mock_uow import MockUoW
from tests.mocks.mock_user_repo import MockUserRepository


@pytest.mark.parametrize(
    ("name", "password", "expected"),
    [
        ("user1", "asdassa2", not_raise()),
        ("user1", "asdassa2", pytest.raises(UserAlreadyExistsError)),
    ],
)
async def test_regiter_user(name, password, expected):
    mock_user_repo = MockUserRepository()
    mock_uow = MockUoW()
    auth_service = AuthService(mock_user_repo, mock_uow)
    inpute_dto = RequestUserDto(username=name, password=password)

    with expected:
        user_in_db = await auth_service.register(inpute_dto)

        assert user_in_db.username == name
        assert isinstance(user_in_db, ResponseUserDto)


@pytest.mark.parametrize(
    ("name", "password", "name_in_db", "password_in_db", "expected"),
    [
        ("user10", "asdassa2", "user10", "asdassa2", not_raise()),
        ("user2", "asdassa2", "user3", "asdassa2", pytest.raises(UserNotFoundError)),
        (
            "user4",
            "asdassa2",
            "user4",
            "asdassa3",
            pytest.raises(UserPasswordNotMatchError),
        ),
    ],
)
async def test_login_user(name, password, name_in_db, password_in_db, expected):
    mock_user_repo = MockUserRepository()
    mock_uow = MockUoW()
    auth_service = AuthService(mock_user_repo, mock_uow)

    inpute_dto_reg = RequestUserDto(username=name, password=password)
    input_dto_log = RequestUserDto(username=name_in_db, password=password_in_db)
    await auth_service.register(inpute_dto_reg)

    with expected:
        user_in_db = await auth_service.login(input_dto_log)

        assert user_in_db.username == name
        assert isinstance(user_in_db, ResponseUserDto)
