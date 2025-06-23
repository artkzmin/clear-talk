from uuid import UUID
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import aliased

from src.core.message.entities import EncryptedMessage
from src.core.message.interfaces import MessageRepositoryInterface

from src.persistence.models.message import MessageModel
from src.persistence.mappers.message import MessageMapper
from src.persistence.repositories.base import BaseRepository


class MessageRepository(
    BaseRepository[MessageModel, EncryptedMessage, MessageMapper],
    MessageRepositoryInterface,
):
    model = MessageModel
    entity = EncryptedMessage
    mapper = MessageMapper

    async def create_message(self, message: EncryptedMessage) -> UUID:
        return await self.create(entity=message)

    async def get_last_message(self, user_id: UUID) -> EncryptedMessage | None:
        stmt_subq = (
            select(MessageModel.previous_message_id)
            .filter(
                MessageModel.user_id == user_id,
                MessageModel.previous_message_id.isnot(None),
            )
            .subquery()
        )
        stmt = (
            select(MessageModel)
            .filter(
                MessageModel.id.notin_(select(stmt_subq)),
                MessageModel.user_id == user_id,
            )
            .limit(1)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.to_entity(model)

    async def get_messages_chain(self, user_id: UUID) -> list[EncryptedMessage]:
        start_stmt = (
            select(MessageModel.id)
            .filter(
                MessageModel.user_id == user_id,
                MessageModel.previous_message_id.is_(None),
            )
            .limit(1)
        )

        start_result = await self.session.execute(start_stmt)
        start_message_id = start_result.scalar_one_or_none()

        if start_message_id is None:
            return []

        recursive_cte = (
            select(MessageModel.id)
            .filter(MessageModel.id == start_message_id)
            .cte(name="message_chain", recursive=True)
        )
        message_alias = aliased(MessageModel)
        recursive_cte = recursive_cte.union_all(
            select(message_alias.id).filter(
                message_alias.previous_message_id == recursive_cte.c.id
            )
        )
        stmt = select(MessageModel).filter(
            MessageModel.id.in_(select(recursive_cte.c.id))
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]

    async def get_count_user_messages_in_datetime_interval(
        self, user_id: UUID, start_date: datetime, end_date: datetime
    ) -> int:
        stmt = select(func.count(MessageModel.id)).filter(
            MessageModel.user_id == user_id,
            MessageModel.created_at >= start_date,
            MessageModel.created_at <= end_date,
        )
        result = await self.session.execute(stmt)
        return result.scalar()
