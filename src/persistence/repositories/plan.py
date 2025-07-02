from sqlalchemy import select
from uuid import UUID
from src.core.plan.entities import Plan, UserPlan
from src.core.plan.enums import PlanType
from src.core.plan.interfaces import PlanRepositoryInterface

from src.persistence.repositories.base import BaseRepository
from src.persistence.models.plan import PlanModel
from src.persistence.mappers.plan import PlanMapper
from src.persistence.models.user import UserModel


class PlanRepository(
    BaseRepository[PlanModel, Plan, PlanMapper], PlanRepositoryInterface
):
    model = PlanModel
    entity = Plan
    mapper = PlanMapper

    async def get_by_type(self, type_: PlanType) -> Plan | None:
        return await self.get_one_or_none(PlanModel.type_ == type_)

    async def get_by_id(self, plan_id: UUID) -> Plan | None:
        return await self.get_one_or_none(PlanModel.id == plan_id)

    async def get_by_user_id(self, user_id: UUID) -> UserPlan | None:
        query = (
            select(
                UserModel.created_at,
                PlanModel.type_,
                PlanModel.days_count,
                PlanModel.max_messages_count,
                PlanModel.max_context_tokens,
                PlanModel.max_output_tokens,
                PlanModel.id,
            )
            .select_from(UserModel)
            .join(PlanModel, UserModel.plan_id == PlanModel.id)
            .filter(UserModel.id == user_id)
        )
        result = await self.session.execute(query)
        row = result.one_or_none()
        if row is None:
            return None
        return UserPlan(
            id=row.id,
            type_=row.type_,
            days_count=row.days_count,
            max_messages_count=row.max_messages_count,
            max_context_tokens=row.max_context_tokens,
            max_output_tokens=row.max_output_tokens,
            plan_activated_at=row.created_at.date(),
        )
