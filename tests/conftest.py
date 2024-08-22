import pytest

from .mocks import MockUrlRepository


@pytest.fixture(scope="session")
def url_repo():
    return MockUrlRepository()
