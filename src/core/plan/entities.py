from pydantic import BaseModel, Field
from datetime import datetime
from src.core.plan.enums import PlanType
from src.core.abc.entities import BaseEntityUUID
from src.core.constants import MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS


class PlanLimits(BaseModel):
    max_messages_count: int = Field(ge=0)
    days_count: int = Field(ge=0)
    max_context_tokens: int = Field(ge=0, le=MAX_CONTEXT_TOKENS)
    max_output_tokens: int = Field(ge=0, le=MAX_OUTPUT_TOKENS)


class Plan(BaseEntityUUID):
    plan_type: PlanType
    limits: PlanLimits


class UserPlan(BaseEntityUUID):
    plan: Plan
    activated_at: datetime
    is_active: bool = Field(default=True)
