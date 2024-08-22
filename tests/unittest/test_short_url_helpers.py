from copy import deepcopy

from app.main.config import UrlConfig
from app.repositories.abstract import UrlRepository
from app.services.dto.dto import ResponseUrlDto
from app.utils.get_short_url import (
    GenerateShortUrl,
    GenerateShortUrls,
    GetShortUrl,
)

test_short_url = "asdas123"
test_response_dto = ResponseUrlDto(
    urlid=1, url="https://www.google.com/", short_url=test_short_url, clics=0, user_id=1
)
test_response_dtos = [
    ResponseUrlDto(
        urlid=1,
        url="https://www.google.com/",
        short_url="xvx234Rwq21312",
        clics=0,
        user_id=1,
    ),
    ResponseUrlDto(
        urlid=2,
        url="https://www.yahoo.com/",
        short_url="juyg123sn&Y2S",
        clics=0,
        user_id=2,
    ),
    ResponseUrlDto(
        urlid=3,
        url="https://www.bing.com/",
        short_url="zxc<KU^Gs12s",
        clics=0,
        user_id=3,
    ),
]
url_config = UrlConfig("localhost", "http")


async def test_get_short_url(url_repo: UrlRepository):
    short_code = await GetShortUrl()(url_repo)
    assert short_code != ""
    assert isinstance(short_code, str)


async def test_generate_short_urls():
    test_response_dto_after_generation = await GenerateShortUrls(url_config)(
        deepcopy(test_response_dtos)
    )
    for i, j in zip(
        test_response_dto_after_generation, test_response_dtos, strict=True
    ):
        assert i.short_url != ""
        assert isinstance(i.short_url, str)
        assert (
            i.short_url
            == f"{url_config.protocol}://{url_config.host}/t/?short={j.short_url}"
        )


async def test_generate_short_url():
    test_response_dto_after_generation = await GenerateShortUrl(url_config)(
        deepcopy(test_response_dto)
    )
    assert test_response_dto_after_generation.short_url != ""
    assert isinstance(test_response_dto_after_generation.short_url, str)
    assert (
        test_response_dto_after_generation.short_url
        == f"{url_config.protocol}://{url_config.host}/t/?short={test_short_url}"
    )
