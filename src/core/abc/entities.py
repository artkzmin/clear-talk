from pydantic import BaseModel, Field
from uuid import UUID
from src.core.constants import STR_ID_LENGTH, INT_ID_MAX_VALUE


class BaseEntityStrID(BaseModel):
    id_: str | None = Field(default=None, min_length=1, max_length=STR_ID_LENGTH)


class BaseEntityUUID(BaseModel):
    id_: UUID | None = None


class BaseEntityIntID(BaseModel):
    id_: int | None = Field(default=None, ge=1, le=INT_ID_MAX_VALUE)
