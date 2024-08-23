import os
from collections.abc import AsyncGenerator, Generator
from pathlib import Path

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .database_command import create_database, database_exists, drop_database
from .mocks import MockUrlRepository

BASE_DIR = Path(__file__).parent.parent
load_dotenv(find_dotenv(".env.test"))


@pytest.fixture(scope="session")
def _migrate() -> Generator[None, None]:
    postgres_url = os.getenv("DB_URI", "sqlite+aiosqlite:///test.db")
    alembic_script = "./conf/alembic.ini"

    alembic_cfg = AlembicConfig(alembic_script)
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        postgres_url,
    )

    upgrade(alembic_cfg, "head")
    yield
    downgrade(alembic_cfg, "base")


@pytest.fixture(scope="session")
async def test_engine() -> AsyncEngine:
    database_url = os.getenv("DB_URI", "sqlite+aiosqlite:///test.db")
    database_params = {"poolclass": NullPool}

    return create_async_engine(database_url, **database_params)


@pytest.fixture(scope="session")
async def async_sessionmaker_test(test_engine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture()
async def async_session(async_sessionmaker_test) -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker_test() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def create_db(test_engine: AsyncEngine, _migrate) -> AsyncGenerator[None, None]:
    test_database_url = (
        "postgresql+psycopg://dimit:2121@localhost:5433/url_test_db_test"
    )

    if not await database_exists(test_database_url, test_engine):
        await create_database(test_database_url, test_engine)

    yield

    if await database_exists(test_database_url, test_engine):
        await drop_database(test_database_url, test_engine)


@pytest.fixture()
def url_repo():
    return MockUrlRepository()
