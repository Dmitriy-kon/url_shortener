from contextlib import nullcontext as not_raise
from unittest.mock import MagicMock

import pytest

from app.main.config import UrlConfig
from app.services.common.exception import (
    UrlAllreadyExistsError,
    UrlNotFoundError,
    UserIsNotAuthorizedError,
    UserNotFoundError,
)
from app.services.dto.dto import (
    RequestDeleteUrlDto,
    RequestInsertUrlDto,
    RequestLimitOffsetUrlDto,
    RequestUpdateUrlDto,
    ResponseUrlDto,
)
from app.services.url_service import UrlService
from app.utils.get_short_url import GenerateShortUrl, GenerateShortUrls, GetShortUrl
from tests.mocks.mock_uow import MockUoW


@pytest.fixture
async def get_url_service(url_repo, user_repo) -> tuple[UrlService, MagicMock]:
    url_config = UrlConfig("localhost", "http")
    mock_token_provider = MagicMock()

    uow = MockUoW()

    url_service = UrlService(
        url_repo=url_repo,
        user_repo=user_repo,
        id_provider=mock_token_provider,
        uow=uow,
        get_short_url=GetShortUrl(),
        generate_short_urls=GenerateShortUrls(url_config),
        generate_short_url=GenerateShortUrl(url_config),
    )
    return url_service, mock_token_provider


@pytest.mark.parametrize(
    ("user_name", "password", "url", "excepted"),
    [
        ("test_user200", "test_password200", "https://example1.com", not_raise()),
        (
            "test_user200",
            "test_password200",
            "https://example1.com",
            pytest.raises(UrlAllreadyExistsError),
        ),
    ],
)
async def test_insert_url(
    user_name, password, url, excepted, user_repo, get_url_service
):
    input_dto = RequestInsertUrlDto(url=url)
    url_service, mock_token_provider = get_url_service

    user_in_db = await user_repo.get_user_by_username(user_name)
    if not user_in_db:
        user = await user_repo.create_user(
            username=user_name,
            hashed_password=password,
        )
    else:
        user = user_in_db

    mock_token_provider.get_current_user_id.return_value = user.uid

    with excepted:
        res = await url_service.insert_url(input_dto)

        assert isinstance(res, ResponseUrlDto)
        assert res.url == url
        assert res.user_id == user.uid


@pytest.mark.parametrize(
    ("user_name", "password", "url"),
    [
        ("test_user201", "test_password201", "https://example1.com"),
        ("test_user202", "test_password202", "https://example2.com"),
    ],
)
async def test_generate_new_short_url(
    user_name, password, url, user_repo, get_url_service
):
    url_service, mock_token_provider = get_url_service

    user_in_db = await user_repo.create_user(
        username=user_name, hashed_password=password
    )
    mock_token_provider.get_current_user_id.return_value = user_in_db.uid
    url_in_db = await url_service.insert_url(RequestInsertUrlDto(url=url))
    url_id = url_in_db.urlid

    input_dto = RequestUpdateUrlDto(urlid=url_id)
    res = await url_service.generate_new_short_url(input_dto)

    assert isinstance(res, ResponseUrlDto)
    assert res.url == url

    with pytest.raises(UrlNotFoundError):
        await url_service.generate_new_short_url(
            input_dto=RequestUpdateUrlDto(urlid=url_id + 9999)
        )
    mock_token_provider.get_current_user_id.return_value = user_in_db.uid + 9999
    with pytest.raises(UserIsNotAuthorizedError):
        await url_service.generate_new_short_url(
            input_dto=RequestUpdateUrlDto(urlid=url_id)
        )


@pytest.mark.parametrize(
    ("user_name", "password", "url"),
    [
        ("test_user208", "test_password201", "https://example1.com"),
        ("test_user209", "test_password202", "https://example2.com"),
    ],
)
async def test_delete_url(user_name, password, url, user_repo, get_url_service):
    url_service, mock_token_provider = get_url_service
    user_in_db = await user_repo.create_user(
        username=user_name, hashed_password=password
    )
    mock_token_provider.get_current_user_id.return_value = user_in_db.uid
    url_in_db = await url_service.insert_url(RequestInsertUrlDto(url=url))
    url_id = url_in_db.urlid

    res = await url_service.delete_url(RequestDeleteUrlDto(urlid=url_id))
    assert isinstance(res, ResponseUrlDto)

    with pytest.raises(UrlNotFoundError):
        await url_service.delete_url(RequestDeleteUrlDto(urlid=url_id))

    with pytest.raises(UrlNotFoundError):
        await url_service.delete_url(RequestDeleteUrlDto(urlid=url_id + 9999))

    url_in_db_2 = await url_service.insert_url(RequestInsertUrlDto(url=url))
    mock_token_provider.get_current_user_id.return_value = user_in_db.uid + 9999
    with pytest.raises(UserIsNotAuthorizedError):
        await url_service.delete_url(RequestDeleteUrlDto(urlid=url_in_db_2.urlid))


@pytest.mark.parametrize(
    ("user_name", "password", "urls"),
    [
        (
            "test_user304",
            "test_password204",
            ["https://example1.com", "https://example2.com"],
        ),
        (
            "test_user305",
            "test_password204",
            ["https://example3.com", "https://example4.com"],
        ),
    ],
)
async def test_get_all_urls(user_name, password, urls, user_repo, get_url_service):
    url_service, mock_token_provider = get_url_service
    user_in_db = await user_repo.create_user(
        username=user_name, hashed_password=password
    )
    mock_token_provider.get_current_user_id.return_value = 912312312
    with pytest.raises(UserNotFoundError):
        await url_service.get_all_user_urls(
            RequestLimitOffsetUrlDto(limit=20, offset=0)
        )

    mock_token_provider.get_current_user_id.return_value = user_in_db.uid

    res_wrong = await url_service.get_all_user_urls(
        RequestLimitOffsetUrlDto(limit=20, offset=0)
    )
    assert isinstance(res_wrong, list)

    for url in urls:
        await url_service.insert_url(RequestInsertUrlDto(url=url))

    res = await url_service.get_all_user_urls(
        RequestLimitOffsetUrlDto(limit=20, offset=0)
    )

    assert len(res) == len(urls)
    assert all(isinstance(url, ResponseUrlDto) for url in res)
