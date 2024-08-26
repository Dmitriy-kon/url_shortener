from contextlib import nullcontext as not_raise

import pytest

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
from tests.mocks.mock_url_repo import MockUrlRepository
from tests.mocks.mock_user_repo import MockUserRepository


