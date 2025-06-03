from pydantic import BaseModel, Field
from uuid import UUID


class BaseEntityStrID(BaseModel):
    id: str = Field(min_length=1, max_length=128)


class BaseEntityUUID(BaseModel):
    id: UUID


class BaseEntityIntID(BaseModel):
    id: int
