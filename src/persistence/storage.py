from typing import Callable
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession

from src.persistence.repositories.plan import PlanRepository
from src.persistence.repositories.message import MessageRepository
from src.persistence.repositories.user import UserRepository
from src.infrastructure.db.engine import session_maker


class Storage:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.plan = PlanRepository(self.session)
        self.user = UserRepository(self.session)
        self.message = MessageRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()


def get_storage() -> Storage:
    return Storage(session_factory=session_maker)


def inject_storage(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with get_storage() as storage:
            return await func(*args, storage=storage, **kwargs)

    return wrapper
