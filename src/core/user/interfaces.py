from uuid import UUID
from typing import Protocol, runtime_checkable
from src.core.user.entities import User
from src.core.abc.interfaces import BaseRepositoryInterface


@runtime_checkable
class UserRepositoryInterface(BaseRepositoryInterface, Protocol):
    async def create_user(self, user: User) -> UUID:
        """
        Raises:
        src.core.user.exceptions.UserAlreadyExistsException:
            If a user with the same ID or external_id already exists.
        """

    async def is_user_exists(self, hashed_external_user_id: str) -> bool: ...

    async def get_user_by_external_id(
        self, hashed_external_user_id: str
    ) -> User | None: ...

    async def get_user_by_id(self, user_id: UUID) -> User | None: ...
