from typing import Protocol, runtime_checkable
from uuid import UUID
from datetime import datetime
from src.core.storage.interfaces import BaseRepositoryInterface
from src.core.plan.entities import Plan, UserPlan
from src.core.plan.enums import PlanType


@runtime_checkable
class PlanRepositoryInterface(BaseRepositoryInterface, Protocol):
    async def get_by_type(self, plan_type: PlanType) -> Plan | None: ...


@runtime_checkable
class UserPlanRepositoryInterface(BaseRepositoryInterface, Protocol):
    async def get_active_plan_for_user(self, user_id: UUID) -> UserPlan | None: ...

    async def update_plan_for_user(self, user_id: UUID, plan_id: UUID) -> None: ...

    async def create_plan_for_user(
        self, user_id: UUID, plan_id: UUID, created_at: datetime
    ) -> UUID: ...
