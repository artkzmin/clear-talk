from abc import ABC
from typing import Generic, Type, TypeVar
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.base import BaseModel
from src.core.abc.entities import BaseEntity
from src.persistence.mappers.base import BaseMapper

ModelType = TypeVar("ModelType", bound=BaseModel)
EntityType = TypeVar("EntityType", bound=BaseEntity)
MapperType = TypeVar("MapperType", bound=BaseMapper[ModelType, EntityType])


class BaseRepository(ABC, Generic[ModelType, EntityType, MapperType]):
    model: Type[ModelType]
    entity: Type[EntityType]
    mapper: MapperType

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self, *filter, **filter_by) -> list[EntityType]:
        stmt = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return [self.mapper.to_entity(model) for model in result.scalars().all()]

    async def get_one_or_none(self, *filter, **filter_by) -> EntityType | None:
        stmt = select(self.model).filter(*filter).filter_by(**filter_by).limit(1)
        result = await self.session.execute(stmt)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.to_entity(model)

    async def create(self, entity: EntityType) -> EntityType:
        stmt = (
            insert(self.model)
            .values(**entity.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().one()
        return self.mapper.to_entity(model)

    async def edit(
        self, entity: EntityType, exclude_unset: bool = False, **filter_by
    ) -> None:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**entity.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
