import asyncio
import sys
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

from tests.mocks.mock_url_repo import MockUrlRepository
from .database_command import (
    create_database,
    database_exists,
    disconnect_users_from_database,
    drop_database,
)
from .setttings import SettingTest

BASE_DIR = Path(__file__).parent.parent
load_dotenv(find_dotenv(".env.test.local"))

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def settings() -> SettingTest:
    return SettingTest()


@pytest.fixture(scope="session", autouse=True)
def _migrate(settings) -> Generator[None, None]:
    """Run migration for Template database"""
    postgres_url = settings.db_config.db_template_url
    alembic_script = "./conf/alembic.ini"

    alembic_cfg = AlembicConfig(alembic_script)
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        postgres_url,
    )

    upgrade(alembic_cfg, "head")
    yield
    # downgrade(alembic_cfg, "base")


@pytest.fixture(scope="session", autouse=True)
async def create_db(settings: SettingTest) -> AsyncGenerator[None, None]:
    test_engine = create_async_engine(
        settings.db_config.db_template_url,
        poolclass=NullPool,
        echo=False,
        isolation_level="AUTOCOMMIT",
    )

    if not await database_exists(settings.db_config.db_test_name, test_engine):
        await create_database(
            settings.db_config.db_test_name,
            test_engine,
            settings.db_config.db_tamplate_name,
        )

    yield

    if await database_exists(settings.db_config.db_test_name, test_engine):
        await disconnect_users_from_database(
            settings.db_config.db_test_name, test_engine
        )
        await drop_database(settings.db_config.db_test_name, test_engine)


@pytest.fixture(scope="session")
async def test_engine(settings) -> AsyncGenerator[AsyncEngine, None]:
    database_url = settings.db_config.db_test_url
    database_params = {"poolclass": NullPool}
    engine = create_async_engine(database_url, **database_params)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="session")
async def async_sessionmaker_test(test_engine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(test_engine, expire_on_commit=False, autoflush=False)


@pytest.fixture()
async def async_session(async_sessionmaker_test) -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker_test() as session:
        yield session


@pytest.fixture()
def url_repo():
    return MockUrlRepository()
