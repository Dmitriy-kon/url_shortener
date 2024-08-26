import pytest

from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.dto.dto import ResponseUserDto
from .data.data_for_user_repo import (
    data_for_change_user,
    data_for_create_user,
    data_for_delete_user,
    data_for_get_user_by_id,
    data_for_get_user_by_username,
)


@pytest.mark.parametrize(("username", "password", "excepted"), data_for_create_user)
async def test_create_user(username, password, excepted, async_session):
    user_repo = UserSqlalchemyRepository(async_session)

    with excepted:
        user = await user_repo.create_user(username, password)
        await async_session.commit()

        assert isinstance(user, ResponseUserDto), "Must return ResponseUserDto"
        assert user.username == username, "Must return same username"
        assert user.hashed_password == password, "Must return same password"


@pytest.mark.parametrize(("username", "password"), data_for_change_user)
async def test_change_user(username, password, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)

    new_username = user_in_db.username + "new_username"
    new_password = user_in_db.hashed_password + "new_password"

    user_after_change_right = await user_repo.change_user(
        user_in_db.uid, new_username, new_password
    )
    user_after_change_wrong = await user_repo.change_user(
        user_in_db.uid + 9999, new_username, new_password
    )

    assert isinstance(
        user_after_change_right, ResponseUserDto
    ), "Must return ResponseUserDto"
    assert user_after_change_right.username == new_username, "Must return same username"
    assert (
        user_after_change_right.hashed_password == new_password
    ), "Must return same password"

    assert user_after_change_wrong is None, "Must return None"


@pytest.mark.parametrize(("username", "password"), data_for_delete_user)
async def test_delete_user(username, password, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)

    result_right = await user_repo.delete_user(user_in_db.uid)
    result_wrong = await user_repo.delete_user(user_in_db.uid + 9999)

    assert result_right, "Must return True"
    assert result_wrong is None, "Must return None"


@pytest.mark.parametrize(("username", "password"), data_for_get_user_by_username)
async def test_get_user_by_username(username, password, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)

    user_in_db_right = await user_repo.get_user_by_username(username)
    user_in_db_wrong = await user_repo.get_user_by_username(username + "wrong")

    assert isinstance(user_in_db_right, ResponseUserDto), "Must return ResponseUserDto"
    assert user_in_db_right == user_in_db, "Must return same user"
    assert user_in_db_wrong is None, "Must return None"


@pytest.mark.parametrize(("username", "password"), data_for_get_user_by_id)
async def test_get_user_by_id(username, password, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)

    user_in_db_right = await user_repo.get_user_by_id(user_in_db.uid)
    user_in_db_wrong = await user_repo.get_user_by_id(user_in_db.uid + 9999)

    assert isinstance(user_in_db_right, ResponseUserDto), "Must return ResponseUserDto"
    assert user_in_db_right == user_in_db, "Must return same user"
    assert user_in_db_wrong is None, "Must return None"
