from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


async def create_database(url: str, engine: AsyncEngine):
    database = url[url.rfind("/") + 1 :]
    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(text(f"CREATE DATABASE {database}"))


async def drop_database(url: str, engine: AsyncEngine):
    database = url[url.rfind("/") + 1 :]

    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level="AUTOCOMMIT")
        query = text(f"DROP DATABASE {database}")

        await conn.execute(query)


async def database_exists(url: str, engine: AsyncEngine) -> bool:
    database = url[url.rfind("/") + 1 :]
    query = text("SELECT 1 FROM pg_database WHERE datname = :dat")
    async with engine.connect() as conn:
        result = await conn.execute(query, {"dat": database})
        for row in result:
            if row[0] == 1:
                return True
    return False
