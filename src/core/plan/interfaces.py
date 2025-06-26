from uuid import UUID
from typing import Protocol, runtime_checkable
from src.core.plan.entities import Plan, UserPlan
from src.core.plan.enums import PlanType
from src.core.abc.interfaces import BaseRepositoryInterface


@runtime_checkable
class PlanRepositoryInterface(BaseRepositoryInterface, Protocol):
    async def get_by_type(self, type_: PlanType) -> Plan | None: ...
    async def get_by_id(self, plan_id: UUID) -> Plan | None: ...
    async def get_by_user_id(self, user_id: UUID) -> UserPlan | None: ...
