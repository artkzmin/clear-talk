from pydantic import Field
from src.core.constants import STR_ID_LENGTH
from src.core.abc.entities import BaseEntityUUID
from src.core.user.enums import ExternalService
from src.core.plan.entities import UserPlan


class User(BaseEntityUUID):
    external_id: str = Field(min_length=1, max_length=STR_ID_LENGTH)
    external_service: ExternalService
    user_plan: UserPlan
