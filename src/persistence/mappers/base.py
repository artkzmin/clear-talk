from typing import Generic, TypeVar
from src.infrastructure.db.base import BaseModel
from src.core.abc.entities import BaseEntity

ModelType = TypeVar("ModelType", bound=BaseModel)
EntityType = TypeVar("EntityType", bound=BaseEntity)


class BaseMapper(Generic[ModelType, EntityType]):
    model_type: type[ModelType]
    entity_type: type[EntityType]

    @classmethod
    def to_model(cls, entity: EntityType) -> ModelType:
        return cls.model_type(entity.model_dump())

    @classmethod
    def to_entity(cls, model: ModelType) -> EntityType:
        return cls.entity_type.model_validate(model, from_attributes=True)
