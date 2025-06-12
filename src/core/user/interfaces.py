from uuid import UUID
from typing import Protocol, runtime_checkable
from src.core.user.entities import User
from src.core.storage.interfaces import BaseRepositoryInterface


@runtime_checkable
class UserRepositoryInterface(BaseRepositoryInterface, Protocol):
    async def create_user(self, user: User) -> UUID: ...

    async def is_user_exists(self, user_id: UUID) -> bool: ...

    async def get_user_by_external_id(self, external_user_id: str) -> User: ...

    async def get_user_by_id(self, user_id: UUID) -> User: ...
