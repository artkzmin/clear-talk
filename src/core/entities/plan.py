from src.core.entities.base import BaseEntityUUID
from src.core.enums import PlanType


class Plan(BaseEntityUUID):
    type: PlanType
