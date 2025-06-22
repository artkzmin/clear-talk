from src.core.interfaces import StorageInterface
from src.core.plan.enums import PlanType
from src.core.plan.entities import Plan
from src.core.plan.exceptions import PlanNotFoundException


class PlanService:
    def __init__(self, storage: StorageInterface) -> None:
        self._storage = storage

    async def get_plan(self, type_: PlanType) -> Plan:
        result = await self._storage.plan.get_by_type(type_=type_)
        if not result:
            raise PlanNotFoundException()
        return result
