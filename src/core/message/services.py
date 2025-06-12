from typing import TypeVar
from uuid import UUID
from datetime import datetime
from src.core.storage.service import StorageService
from src.core.message.entities import BaseMessageInput, Message
from src.core.message.enums import MessageSenderType
from src.core.message.exceptions import (
    LastMessageSenderRepeatsException,
    CannotCreateSystemMessageException,
)

T = TypeVar("T", bound=BaseMessageInput)


class MessageService:
    def __init__(self, storage: StorageService):
        self.storage = storage

    async def _add_message(
        self,
        message_input: T,
        user_id: UUID,
        message_sender_type: MessageSenderType,
        commit: bool = False,
    ) -> UUID:
        last_message = await self.storage.message.get_last_message(user_id)
        if last_message is not None:
            if last_message.sender_type == message_sender_type:
                raise LastMessageSenderRepeatsException(sender_type=message_sender_type)
            previous_message_id = last_message.id_
        else:
            previous_message_id = None
        message = Message(
            content=await message_input.as_str(),
            sender_type=message_sender_type,
            previous_message_id=previous_message_id,
        )

        message_id = await self.storage.message.create_message(message)
        if commit:
            await self.storage.commit()
        return message_id

    async def add_user_message(
        self, message_input: T, user_id: UUID, commit: bool = False
    ) -> UUID:
        return await self._add_message(
            message_input=message_input,
            user_id=user_id,
            message_sender_type=MessageSenderType.USER,
            commit=commit,
        )

    async def add_assistant_message(
        self, message_input: T, user_id: UUID, commit: bool = False
    ) -> UUID:
        return await self._add_message(
            message_input=message_input,
            user_id=user_id,
            message_sender_type=MessageSenderType.ASSISTANT,
            commit=commit,
        )

    async def add_system_message(
        self, user_id: UUID, system_message_content: str, commit: bool = False
    ) -> UUID:
        last_message = await self.storage.message.get_last_message(user_id)
        if last_message is not None:
            raise CannotCreateSystemMessageException()
        message = Message(
            content=system_message_content, sender_type=MessageSenderType.SYSTEM
        )
        message_id = await self.storage.message.create_message(message)
        if commit:
            await self.storage.commit()
        return message_id

    async def edit_all_system_messages_content(
        self, new_content: str, commit: bool = False
    ) -> None:
        await self.storage.message.update_all_system_messages_content(new_content)
        if commit:
            await self.storage.commit()

    async def get_messages_chain(self, user_id: UUID) -> list[Message]:
        messages = await self.storage.message.get_messages_chain(user_id)
        return messages

    async def get_count_user_messages_in_datetime_interval(
        self, user_id: UUID, start_date: datetime, end_date: datetime
    ) -> int:
        return await self.storage.message.get_count_user_messages_in_datetime_interval(
            user_id=user_id, start_date=start_date, end_date=end_date
        )
