from pydantic import Field
from uuid import UUID
from datetime import datetime
from src.core.constants import STR_ID_LENGTH, STR_HASH_LENGTH
from src.core.abc.entities import BaseEntityUUID, BaseEntity
from src.core.user.enums import ExternalServiceType


class InputUser(BaseEntity):
    external_id: str = Field(min_length=1, max_length=STR_ID_LENGTH)
    external_service: ExternalServiceType


class User(BaseEntityUUID):
    hashed_external_id: str = Field(
        min_length=STR_HASH_LENGTH, max_length=STR_HASH_LENGTH
    )
    external_service: ExternalServiceType
    created_at: datetime
    plan_id: UUID
    plan_activated_at: datetime
