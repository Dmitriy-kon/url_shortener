import pytest

from app.services.dto.dto import (
    ResponseUrlDto,
)
from app.services.get_short_url import GetUrlFromShortUrl
from tests.mocks.mock_uow import MockUoW


@pytest.mark.parametrize(
    ("username", "password", "url", "short_url"),
    [
        (
            "test_user900",
            "test_password200",
            "https://examplezxczxcs.com",
            "zxczxcasd12312",
        ),
        (
            "test_user901",
            "test_password2022",
            "https://examplezxSD@czxcs.com",
            "zxczxcJ&@2312",
        ),
    ],
)
async def test_get_url_from_short_url(
    username, password, url, short_url, url_repo, user_repo
):
    uow = MockUoW()
    get_url = GetUrlFromShortUrl(url_repo=url_repo, uow=uow)

    user_in_db = await user_repo.create_user(
        username=username, hashed_password=password
    )
    url_in_db = await url_repo.insert_url(
        url=url, user_id=user_in_db.uid, short_url=short_url
    )

    res_right = await get_url(short_url=short_url)

    assert res_right == url_in_db
    assert url_in_db.clics == 1
    assert isinstance(res_right, ResponseUrlDto)

    res_wrong = await get_url(short_url=short_url + "wrong")
    assert res_wrong is None
