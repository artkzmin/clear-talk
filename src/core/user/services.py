from uuid import UUID
from src.core.storage.service import StorageService
from src.core.user.entities import User
from src.core.plan.enums import PlanType
from src.core.plan.services import PlanService, UserPlanService
from src.core.message.services import MessageService
from src.core.user.exceptions import UserNotFoundException
from src.core.token.services import TokenService


class UserService:
    def __init__(
        self,
        storage: StorageService,
        plan_service: type[PlanService],
        user_plan_service: type[UserPlanService],
        message_service: type[MessageService],
        token_service: type[TokenService],
    ) -> None:
        self.storage = storage
        self.plan_service = plan_service(storage=storage)
        self.user_plan_service = user_plan_service(
            storage=storage,
            message_service=message_service,
            plan_service=plan_service,
            token_service=token_service,
        )
        self.message_service = message_service(storage=storage)

    async def add_user_with_plan_and_system_message(
        self, user: User, system_message_content: str
    ) -> UUID:
        user_id = await self.storage.user.create_user(user)
        plan_id = await self.plan_service.get_plan(type_=PlanType.FREE)
        await self.user_plan_service.create_plan_for_user(
            user_id=user_id, plan_id=plan_id
        )
        await self.message_service.add_system_message(
            user_id=user_id, system_message_content=system_message_content
        )
        await self.storage.commit()
        return user_id

    async def check_user_exists(self, user_id: UUID) -> None:
        if not await self.storage.user.is_user_exists(user_id) > 0:
            raise UserNotFoundException()

    async def get_user_by_external_id(self, external_user_id: str) -> User:
        return await self.storage.user.get_user_by_external_id(external_user_id)

    async def get_user_by_id(self, user_id: UUID) -> User:
        return await self.storage.user.get_user_by_id(user_id)
