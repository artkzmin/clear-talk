from datetime import datetime
from uuid import UUID
from src.core.interfaces import StorageInterface
from src.core.user.entities import InputUser, User
from src.core.plan.enums import PlanType
from src.core.plan.services import PlanService
from src.core.user.exceptions import UserNotFoundException, UserAlreadyExistsException
from src.core.interfaces import HasherUtilityInterface


class UserService:
    def __init__(
        self, storage: StorageInterface, hasher_utility: HasherUtilityInterface
    ) -> None:
        self._storage = storage
        self._plan_service = PlanService(storage=storage)
        self._hasher = hasher_utility

    async def create_user(self, input_user: InputUser) -> User:
        """
        Raises:
            src.core.user.exceptions.UserAlreadyExistsException:
                If a user with the same ID or external_id already exists.
        """
        plan = await self._plan_service.get_plan_by_type(type_=PlanType.FREE)
        now = datetime.now()
        user = User(
            hashed_external_id=self._hasher.get_hash(input_user.external_id),
            external_service=input_user.external_service,
            created_at=now,
            plan_id=plan.id,
            plan_activated_at=now,
        )
        try:
            user_id = await self._storage.user.create_user(user)
        except UserAlreadyExistsException as e:
            raise e

        await self._storage.commit()
        user.id = user_id
        return user

    async def is_user_exists(self, external_user_id: str) -> bool:
        hashed_external_user_id = self._hasher.get_hash(external_user_id)
        return await self._storage.user.is_user_exists(hashed_external_user_id)

    async def get_user_by_external_id(self, external_user_id: str) -> User:
        hashed_external_user_id = self._hasher.get_hash(external_user_id)
        user = await self._storage.user.get_user_by_external_id(hashed_external_user_id)
        if user is None:
            raise UserNotFoundException()
        return user

    async def get_or_create_external_user(self, input_user: InputUser) -> User:
        if await self.is_user_exists(input_user.external_id):
            return await self.get_user_by_external_id(input_user.external_id)
        return await self.create_user(input_user)

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self._storage.user.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundException()
        return user
