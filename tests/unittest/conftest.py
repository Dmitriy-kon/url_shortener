from os import getenv

import pytest

from app.main.config import JwtConfig
from app.utils.datetime_provide import SystemDateTime, Timezone


@pytest.fixture(scope="session")
def jwt_config():
    return JwtConfig(
        secret_key=getenv("SECRET_KEY", "None"),
        expire=int(getenv("EXPIRE", "5")),
        algorithm=getenv("ALGORITHM", "HS256"),
    )


@pytest.fixture
def system_date_time():
    return SystemDateTime(timezone=Timezone.UTC)
