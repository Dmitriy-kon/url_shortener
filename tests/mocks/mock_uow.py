from app.services.abstraction.uow import UoW


class MockUoW(UoW):
    async def commit(self) -> None:
        pass

    async def flush(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
