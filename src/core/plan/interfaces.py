from typing import Protocol, runtime_checkable
from src.core.plan.entities import Plan
from src.core.plan.enums import PlanType
from src.core.abc.interfaces import BaseRepositoryInterface


@runtime_checkable
class PlanRepositoryInterface(BaseRepositoryInterface, Protocol):
    async def get_by_type(self, type_: PlanType) -> Plan | None: ...
