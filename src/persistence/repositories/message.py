from uuid import UUID
from datetime import date, timedelta
from sqlalchemy import select, func

from src.core.message.entities import EncryptedMessage
from src.core.message.enums import MessageSenderType
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
        return (await self.create(entity=message)).id

    async def get_last_message(self, user_id: UUID) -> EncryptedMessage | None:
        query = (
            select(MessageModel)
            .filter(
                MessageModel.user_id == user_id,
            )
            .order_by(MessageModel.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.to_entity(model)

    async def get_messages_chain(self, user_id: UUID) -> list[EncryptedMessage]:
        query = (
            select(MessageModel)
            .filter(
                MessageModel.user_id == user_id,
            )
            .order_by(MessageModel.created_at.asc())
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]

    async def get_count_user_messages_in_date_interval(
        self, user_id: UUID, start_date: date, end_date: date
    ) -> int:
        query = select(func.count(MessageModel.id)).filter(
            MessageModel.user_id == user_id,
            MessageModel.created_at >= start_date,
            MessageModel.created_at <= end_date + timedelta(days=1),
            MessageModel.sender == MessageSenderType.USER,
        )
        result = await self.session.execute(query)
        return result.scalar()
