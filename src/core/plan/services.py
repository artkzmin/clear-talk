from uuid import UUID
from datetime import datetime, timedelta
from src.core.storage.service import StorageService
from src.core.plan.enums import PlanType
from src.core.plan.entities import Plan, UserPlan
from src.core.plan.exceptions import (
    ActiveUserPlanNotFoundException,
    PlanNotFoundException,
    UserPlanExceededLimitException,
    UserPlanExceededContextTokensException,
)
from src.core.message.services import MessageService
from src.core.message.entities import Message
from src.core.token.services import TokenService


class PlanService:
    def __init__(self, storage: StorageService) -> None:
        self.storage = storage

    async def get_plan(self, plan_type: PlanType) -> Plan:
        result = await self.storage.plan.get_by_type(plan_type=plan_type)
        if not result:
            raise PlanNotFoundException()
        return result


class UserPlanService:
    def __init__(
        self,
        storage: StorageService,
        message_service: type[MessageService],
        plan_service: type[PlanService],
        token_service: type[TokenService],
    ) -> None:
        self.storage = storage
        self.plan_service = plan_service(storage=storage)
        self.message_service = message_service(storage=storage)
        self.token_service = token_service()

    async def get_active_user_plan(self, user_id: UUID) -> UserPlan:
        result = await self.storage.user_plan.get_active_plan_for_user(user_id=user_id)
        if not result:
            raise ActiveUserPlanNotFoundException()
        return result

    async def edit_plan_for_user(
        self, user_id: UUID, plan_type: PlanType, commit: bool = False
    ) -> None:
        plan = await self.plan_service.get_plan(plan_type)
        await self.storage.user_plan.update_plan_for_user(
            user_id=user_id, plan_id=plan.id_
        )
        if commit:
            await self.storage.commit()

    async def check_user_plan(self, user_id: UUID, new_user_message: Message) -> None:
        user_plan = await self.get_active_user_plan(user_id=user_id)

        count_user_messages_in_interval = (
            await self.message_service.get_count_user_messages_in_datetime_interval(
                user_id=user_id,
                start_date=user_plan.created_at,
                end_date=user_plan.created_at
                + timedelta(days=user_plan.plan.limits.days_count),
            )
        )
        if count_user_messages_in_interval >= user_plan.plan.limits.max_messages_count:
            raise UserPlanExceededLimitException()

        all_messages = await self.message_service.get_messages_chain(user_id=user_id)
        all_messages.append(new_user_message)
        context_tokens = self.token_service.get_tokens_count(all_messages)
        if context_tokens > user_plan.plan.limits.max_context_tokens:
            raise UserPlanExceededContextTokensException()

    async def create_plan_for_user(
        self, user_id: UUID, plan_type: PlanType, commit: bool = False
    ) -> None:
        plan = await self.plan_service.get_plan(plan_type=plan_type)
        await self.storage.user_plan.create_plan_for_user(
            user_id=user_id,
            plan_id=plan.id_,
            created_at=datetime.now(),
        )
        if commit:
            await self.storage.commit()
