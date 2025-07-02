from uuid import UUID
from src.core.plan.services import PlanService
from src.persistence.storage import inject_storage, Storage
from src.core.plan.entities import UserPlan


@inject_storage
async def get_plan_by_user_id(user_id: UUID, storage: Storage) -> UserPlan:
    return await PlanService(storage=storage).get_user_plan_by_user_id(user_id)
