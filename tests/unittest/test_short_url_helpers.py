from typing import ClassVar
from unittest.mock import patch

import pytest
from src.app.main.config import UrlConfig
from src.app.repositories.url_repo import UrlSqlalchemyRepository
from src.app.services.dto.dto import ResponseUrlDto
from src.app.utils.get_short_url import (
    GenerateShortUrl,
    GenerateShortUrls,
    GetShortUrl,
)

test_short_url = "asdas123"
test_response_dto = ResponseUrlDto(
    urlid=1, url="https://www.google.com/", short_url=test_short_url, clics=0, user_id=1
)
url_config = UrlConfig("localhost", "http")


class MockUrlSqlalchemyRepository(UrlSqlalchemyRepository):
    data: ClassVar[dict] = {test_short_url: test_response_dto}

    async def get_url_by_short_url(self, short_url: str) -> ResponseUrlDto | None:
        return self.data.get(short_url)

async def test_get_short_url() -> None:
    get_short_url = GetShortUrl(url_config)
    url_repo = MockUrlSqlalchemyRepository()

    res = await get_short_url(MockUrlSqlalchemyRepository())
