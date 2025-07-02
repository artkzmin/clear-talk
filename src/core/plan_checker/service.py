from datetime import timedelta, date
from uuid import UUID
from src.core.plan.services import PlanService
from src.core.message.services import MessageService
from src.core.interfaces import StorageInterface
from src.core.interfaces import EncryptorUtilityInterface
from src.core.plan_checker.exceptions import (
    PlanNotActiveException,
    PlanMessagesCountLimitException,
    PlanTokensLimitException,
)
from src.core.plan_checker.interfaces import TokenUtilityInterface
from src.core.interfaces import HasherUtilityInterface
from src.core.message.entities import InputMessage


class PlanCheckerService:
    def __init__(
        self,
        storage: StorageInterface,
        encryptor_utility: EncryptorUtilityInterface,
        token_utility: TokenUtilityInterface,
        hasher_utility: HasherUtilityInterface,
    ) -> None:
        self._storage = storage
        self._message_service = MessageService(
            storage=storage, encryptor=encryptor_utility
        )
        self._token_utility = token_utility
        self._plan_service = PlanService(storage=storage)

    async def check_plan_for_new_message(self, message_input: InputMessage) -> None:
        """
        Raises:
            src.core.plan_checker.exceptions.PlanNotActiveException:
                If the plan is not active.
            src.core.plan_checker.exceptions.PlanMessagesCountLimitException:
                If the plan has reached the maximum number of messages.
            src.core.plan_checker.exceptions.PlanTokensLimitException:
                If the plan has reached the maximum number of tokens.
        """
        user_plan = await self._plan_service.get_user_plan_by_user_id(
            user_id=message_input.user_id
        )

        if user_plan.days_count is not None:
            if not await self._is_plan_active(
                plan_activated_at=user_plan.plan_activated_at,
                plan_days_count=user_plan.days_count,
            ):
                raise PlanNotActiveException()

        if user_plan.max_messages_count is not None:
            if not await self._is_plan_has_messages_count(
                user_id=message_input.user_id,
                plan_activated_at=user_plan.plan_activated_at,
                plan_max_messages_count=user_plan.max_messages_count,
            ):
                raise PlanMessagesCountLimitException()

        if user_plan.max_context_tokens is not None:
            if not await self._is_plan_has_tokens_limit(
                message_input=message_input,
                plan_max_tokens_count=user_plan.max_context_tokens,
            ):
                raise PlanTokensLimitException()

    async def _is_plan_active(
        self, plan_activated_at: date, plan_days_count: int
    ) -> bool:
        return plan_activated_at + timedelta(days=plan_days_count) > date.today()

    async def _is_plan_has_messages_count(
        self,
        user_id: UUID,
        plan_activated_at: date,
        plan_max_messages_count: int,
    ) -> bool:
        return (
            await self._message_service.get_count_user_messages_in_date_interval(
                user_id=user_id,
                start_date=plan_activated_at,
                end_date=date.today(),
            )
            < plan_max_messages_count
        )

    async def _is_plan_has_tokens_limit(
        self, message_input: InputMessage, plan_max_tokens_count: int
    ) -> bool:
        messages_chain = await self._message_service.get_messages_chain(
            message_input.user_id
        )

        tokens_count = 0
        for m in messages_chain:
            tokens_count += self._token_utility.get_tokens_count(m.content)
        tokens_count += self._token_utility.get_tokens_count(message_input.content)
        return tokens_count <= plan_max_tokens_count
