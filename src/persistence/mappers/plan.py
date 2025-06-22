from src.persistence.mappers.base import BaseMapper
from src.persistence.models.plan import PlanModel
from src.core.plan.entities import Plan


class PlanMapper(BaseMapper[PlanModel, Plan]):
    entity_type = Plan
    model_type = PlanModel
