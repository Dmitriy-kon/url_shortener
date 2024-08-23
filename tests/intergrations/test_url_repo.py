import pytest

from app.repositories.url_repo import UrlSqlalchemyRepository
from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.dto.dto import ResponseUrlDto
from .data.data_for_url_repo import data_for_insert_test


@pytest.mark.parametrize(
    ("username", "password", "url", "short_url", "excepted"), data_for_insert_test
)
async def test_insert_url(username, password, url, short_url, excepted, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user = await user_repo.create_user(username, password)
    await async_session.commit()

    url_repo = UrlSqlalchemyRepository(async_session)

    with excepted:
        url_in_db = await url_repo.insert_url(url, short_url, user.uid)
        await async_session.commit()

        user_update = await user_repo.get_user_by_id(user.uid)

        assert url_in_db is not None, "Url should be inserted"
        assert isinstance(url_in_db, ResponseUrlDto), "Url should be a ResponseUrlDto"
        assert url_in_db.url == url, "Url should be the same"
        assert url_in_db.short_url == short_url, "Short url should be the same"
        assert url_in_db.user_id == user.uid, "User id should be the same"
        assert user_update.urls[0] == url_in_db, "User urls should be the same"
