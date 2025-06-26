from uuid import UUID
from src.core.interfaces import StorageInterface
from src.core.plan.enums import PlanType
from src.core.plan.entities import Plan, UserPlan
from src.core.plan.exceptions import PlanNotFoundException


class PlanService:
    def __init__(self, storage: StorageInterface) -> None:
        self._storage = storage

    async def get_plan_by_type(self, type_: PlanType) -> Plan:
        result = await self._storage.plan.get_by_type(type_=type_)
        if not result:
            raise PlanNotFoundException()
        return result

    async def get_plan_by_id(self, plan_id: UUID) -> Plan:
        result = await self._storage.plan.get_by_id(plan_id=plan_id)
        if not result:
            raise PlanNotFoundException()
        return result

    async def get_user_plan_by_user_id(self, user_id: UUID) -> UserPlan:
        result = await self._storage.plan.get_by_user_id(user_id=user_id)
        if not result:
            raise PlanNotFoundException()
        return result
