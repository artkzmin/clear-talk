from pydantic import BaseModel, Field
from uuid import UUID
from src.core.constants import STR_ID_LENGTH, INT_ID_MAX_VALUE


class BaseEntity(BaseModel):
    pass


class BaseEntityStrID(BaseEntity):
    id: str | None = Field(default=None, min_length=1, max_length=STR_ID_LENGTH)


class BaseEntityUUID(BaseEntity):
    id: UUID | None = None


class BaseEntityIntID(BaseEntity):
    id: int | None = Field(default=None, ge=1, le=INT_ID_MAX_VALUE)
