from uuid import UUID
from src.core.plan.services import PlanService
from src.persistence.storage import inject_storage, Storage
from src.core.plan.entities import UserPlan, Plan
from src.core.plan_checker.entities import RemainingUserPlan
from src.core.plan_checker.service import PlanCheckerService
from src.core.plan.enums import PlanType
from src.application.services.user import get_telegram_user
from src.infrastructure.utils.encryptor import FernetEncryptorUtility
from src.infrastructure.utils.token import TiktokenTokenUtility
from src.infrastructure.utils.hasher import HmacSha256Hasher


@inject_storage
async def _get_user_plan(user_id: UUID, storage: Storage) -> UserPlan:
    return await PlanService(storage=storage).get_user_plan_by_user_id(user_id)


async def get_user_plan(user_id: UUID) -> UserPlan:
    return await _get_user_plan(user_id)


async def get_user_plan_by_telegram_user_id(
    telegram_user_id: int,
) -> UserPlan:
    """
    Raises:
        src.core.plan.exceptions.PlanNotFoundException:
            If the plan is not found.
    """
    user = await get_telegram_user(telegram_user_id)
    return await get_user_plan(user_id=user.id)


@inject_storage
async def _get_remaining_user_plan(
    user_id: UUID, storage: Storage
) -> RemainingUserPlan:
    return await PlanCheckerService(
        storage=storage,
        encryptor_utility=FernetEncryptorUtility(),
        token_utility=TiktokenTokenUtility(),
        hasher_utility=HmacSha256Hasher(),
    ).get_remaining_user_plan(user_id)


async def get_remaining_user_plan(user_id: UUID) -> RemainingUserPlan:
    return await _get_remaining_user_plan(user_id)


@inject_storage
async def _get_plan_by_type(type_: PlanType, storage: Storage) -> Plan:
    return await PlanService(storage=storage).get_plan_by_type(type_)


async def get_plan_by_type(type_: PlanType) -> Plan:
    return await _get_plan_by_type(type_)


async def get_pro_plan() -> Plan:
    return await _get_plan_by_type(PlanType.PRO)
