from uuid import UUID
from datetime import datetime
from src.core.interfaces import StorageInterface
from src.core.message.entities import EncryptedMessage, InputMessage, DecryptedMessage
from src.core.message.enums import MessageSenderType
from src.core.message.exceptions import LastMessageSenderRepeatsException
from src.core.interfaces import EncryptorUtilityInterface


class MessageService:
    def __init__(self, storage: StorageInterface, encryptor: EncryptorUtilityInterface):
        self._storage = storage
        self._encryptor = encryptor

    async def _create_message(
        self,
        message: InputMessage,
        sender: MessageSenderType,
        commit: bool = False,
    ) -> UUID:
        last_message = await self._storage.message.get_last_message(message.user_id)
        if last_message is not None:
            if last_message.sender == sender:
                raise LastMessageSenderRepeatsException(sender=sender)
            previous_message_id = last_message.id
        else:
            previous_message_id = None
        message = EncryptedMessage(
            encrypted_content=self._encryptor.encrypt(message.content),
            sender=sender,
            previous_message_id=previous_message_id,
            user_id=message.user_id,
            created_at=datetime.now(),
        )

        message_id = await self._storage.message.create_message(message)
        if commit:
            await self._storage.commit()
        return message_id

    async def create_user_message(
        self, message: InputMessage, commit: bool = False
    ) -> UUID:
        return await self._create_message(
            message=message,
            sender=MessageSenderType.USER,
            commit=commit,
        )

    async def create_assistant_message(
        self, message: InputMessage, commit: bool = False
    ) -> UUID:
        return await self._create_message(
            message=message,
            sender=MessageSenderType.ASSISTANT,
            commit=commit,
        )

    async def get_messages_chain(self, user_id: UUID) -> list[DecryptedMessage]:
        messages_chain = await self._storage.message.get_messages_chain(user_id)
        return [
            DecryptedMessage(
                id=m.id,
                sender=m.sender,
                content=self._encryptor.decrypt(m.encrypted_content),
                previous_message_id=m.previous_message_id,
                user_id=m.user_id,
                created_at=m.created_at,
            )
            for m in messages_chain
        ]

    async def get_count_user_messages_in_datetime_interval(
        self, user_id: UUID, start_date: datetime, end_date: datetime
    ) -> int:
        return await self._storage.message.get_count_user_messages_in_datetime_interval(
            user_id=user_id, start_date=start_date, end_date=end_date
        )
