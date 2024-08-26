import pytest

from app.repositories.url_repo import UrlSqlalchemyRepository
from app.repositories.user_repo import UserSqlalchemyRepository
from app.services.dto.dto import ResponseUrlDto
from .data.data_for_url_repo import (
    data_for_all_user_urls_test,
    data_for_change_test,
    data_for_click_url_test,
    data_for_delete_test,
    data_for_get_url_by_short_url,
    data_for_get_url_by_url_id,
    data_for_get_url_by_userid_and_url,
    data_for_insert_test,
)


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


@pytest.mark.parametrize(
    ("username", "password", "url", "short_url"), data_for_change_test
)
async def test_change_url(username, password, url, short_url, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)
    await async_session.commit()

    url_repo = UrlSqlalchemyRepository(async_session)

    url_in_db = await url_repo.insert_url(url, short_url, user_in_db.uid)
    await async_session.commit()

    new_short_url = "new_short_url"
    url_change_right = await url_repo.change_url(url_in_db.urlid, new_short_url)
    url_change_wrong = await url_repo.change_url(url_in_db.urlid + 9999, new_short_url)

    assert isinstance(
        url_change_right, ResponseUrlDto
    ), "Url should be a ResponseUrlDto"
    assert url_change_right.short_url == new_short_url, "Short url should be the same"
    assert url_change_wrong is None, "Url should not be changed"


@pytest.mark.parametrize(
    ("username", "password", "url", "short_url"), data_for_click_url_test
)
async def test_update_url_click(username, password, url, short_url, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)
    await async_session.commit()

    url_repo = UrlSqlalchemyRepository(async_session)

    url_in_db = await url_repo.insert_url(url, short_url, user_in_db.uid)
    await async_session.commit()

    url_click_right = await url_repo.update_url_clicks(url_in_db.urlid)
    await async_session.commit()
    url_click_wrong = await url_repo.update_url_clicks(url_in_db.urlid + 9999)

    assert isinstance(url_click_right, ResponseUrlDto), "Url should be a ResponseUrlDto"
    assert url_click_right.clics == 1, "Clics should be 1"
    assert url_click_wrong is None, "Clics should be None"


@pytest.mark.parametrize(
    ("username", "password", "url", "short_url"), data_for_delete_test
)
async def test_delete_url(username, password, url, short_url, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)
    await async_session.commit()

    url_repo = UrlSqlalchemyRepository(async_session)
    url_in_db = await url_repo.insert_url(url, short_url, user_in_db.uid)
    await async_session.commit()

    url_delete_right = await url_repo.delete_url(url_in_db.urlid)
    url_delete_wrong = await url_repo.delete_url(url_in_db.urlid + 9999)

    assert isinstance(url_delete_right, ResponseUrlDto), "Must return ResponseUrlDto"
    assert url_delete_right.urlid == url_in_db.urlid, "Must return same urlid"
    assert url_delete_wrong is None, "Must return None"


@pytest.mark.parametrize(
    ("username", "password", "urls", "limit", "offset"), data_for_all_user_urls_test
)
async def test_get_all_user_urls(
    username, password, urls, limit, offset, async_session
):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)
    await async_session.commit()

    url_repo = UrlSqlalchemyRepository(async_session)
    for url in urls:
        await url_repo.insert_url(url[0], url[1], user_in_db.uid)
    await async_session.commit()

    user_urls_right = await url_repo.get_all_user_urls(user_in_db.uid, limit, offset)
    user_urls_wrong = await url_repo.get_all_user_urls(
        user_in_db.uid + 9999, limit, offset
    )
    assert len(user_urls_right) == (
        len(urls) - offset
    ), "Must return same amount of urls"
    assert all(
        isinstance(url, ResponseUrlDto) for url in user_urls_right
    ), "Must return ResponseUrlDto"
    assert user_urls_wrong is None, "Must return None"


@pytest.mark.parametrize(
    ("username", "password", "url", "short_url"), data_for_get_url_by_short_url
)
async def test_get_url_by_short_url(username, password, url, short_url, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)
    await async_session.commit()

    url_repo = UrlSqlalchemyRepository(async_session)
    url_in_db = await url_repo.insert_url(url, short_url, user_in_db.uid)
    await async_session.commit()

    url_get_short_right = await url_repo.get_url_by_short_url(short_url)
    url_get_short_wrong = await url_repo.get_url_by_short_url(short_url + "wrong")

    assert isinstance(url_get_short_right, ResponseUrlDto), "Must return ResponseUrlDto"
    assert url_get_short_right.user_id == user_in_db.uid, "Must return same user_id"
    assert url_get_short_right.urlid == url_in_db.urlid, "Must return same urlid"
    assert url_get_short_wrong is None, "Must return None"


@pytest.mark.parametrize(
    ("username", "password", "url", "short_url"), data_for_get_url_by_userid_and_url
)
async def test_get_url_by_userid_and_url(
    username, password, url, short_url, async_session
):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)
    await async_session.commit()

    url_repo = UrlSqlalchemyRepository(async_session)
    url_in_db = await url_repo.insert_url(url, short_url, user_in_db.uid)
    await async_session.commit()

    url_get_user_right = await url_repo.get_url_by_userid_and_url(user_in_db.uid, url)
    url_get_user_wrong = await url_repo.get_url_by_userid_and_url(
        user_in_db.uid + 9999, url
    )

    assert isinstance(url_get_user_right, ResponseUrlDto), "Must return ResponseUrlDto"
    assert url_get_user_right.user_id == user_in_db.uid, "Must return same user_id"
    assert url_get_user_right.urlid == url_in_db.urlid, "Must return same urlid"
    assert url_get_user_wrong is None, "Must return None"


@pytest.mark.parametrize(
    ("username", "password", "url", "short_url"), data_for_get_url_by_url_id
)
async def test_get_url_by_url_id(username, password, url, short_url, async_session):
    user_repo = UserSqlalchemyRepository(async_session)
    user_in_db = await user_repo.create_user(username, password)
    await async_session.commit()

    url_repo = UrlSqlalchemyRepository(async_session)
    url_in_db = await url_repo.insert_url(url, short_url, user_in_db.uid)
    await async_session.commit()

    url_get_by_id_right = await url_repo.get_url_by_url_id(url_in_db.urlid)
    url_get_by_id_wrong = await url_repo.get_url_by_url_id(url_in_db.urlid + 9999)

    assert isinstance(url_get_by_id_right, ResponseUrlDto), "Must return ResponseUrlDto"
    assert url_get_by_id_right.user_id == user_in_db.uid, "Must return same user_id"
    assert url_get_by_id_right.urlid == url_in_db.urlid, "Must return same urlid"
    assert url_get_by_id_wrong is None, "Must return None"
