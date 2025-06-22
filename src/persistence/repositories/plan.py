from src.core.plan.entities import Plan
from src.core.plan.enums import PlanType
from src.core.plan.interfaces import PlanRepositoryInterface

from src.persistence.repositories.base import BaseRepository
from src.persistence.models.plan import PlanModel
from src.persistence.mappers.plan import PlanMapper


class PlanRepository(
    BaseRepository[PlanModel, Plan, PlanMapper], PlanRepositoryInterface
):
    model = PlanModel
    entity = Plan
    mapper = PlanMapper

    async def get_by_type(self, type_: PlanType) -> Plan | None:
        return await self.get_one_or_none(PlanModel.type_ == type_)
