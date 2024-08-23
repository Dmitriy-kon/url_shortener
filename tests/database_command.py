from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


async def create_database(db_name: str, engine: AsyncEngine, template: str) -> None:
    if not template:
        template = "template0"
    async with engine.connect() as conn:
        await conn.execute(
            text(f"CREATE DATABASE {db_name} ENCODING 'utf-8' TEMPLATE {template}")
        )


async def disconnect_users_from_database(database: str, engine: AsyncEngine):
    async with engine.connect() as conn:
        query = text("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = :dat
    AND pid <> pg_backend_pid();
            """)
        await conn.execute(query, {"dat": database})


async def drop_database(url: str, engine: AsyncEngine):
    database = url[url.rfind("/") + 1 :]

    async with engine.connect() as conn:
        query = text(f"DROP DATABASE {database}")

        await conn.execute(query)


async def database_exists(database: str, engine: AsyncEngine) -> bool:
    query = text("SELECT 1 FROM pg_database WHERE datname = :dat")
    async with engine.connect() as conn:
        result = await conn.execute(query, {"dat": database})
        for row in result:
            if row[0] == 1:
                return True
    return False
