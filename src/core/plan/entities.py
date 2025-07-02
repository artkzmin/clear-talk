from datetime import date
from pydantic import Field

from src.core.plan.enums import PlanType
from src.core.abc.entities import BaseEntityUUID
from src.core.constants import MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS


class Plan(BaseEntityUUID):
    type_: PlanType
    days_count: int | None = Field(ge=0)
    max_messages_count: int | None = Field(ge=0)
    max_context_tokens: int | None = Field(ge=0, le=MAX_CONTEXT_TOKENS)
    max_output_tokens: int | None = Field(ge=0, le=MAX_OUTPUT_TOKENS)


class UserPlan(Plan):
    plan_activated_at: date
