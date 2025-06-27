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
        input_message: InputMessage,
        sender: MessageSenderType,
        commit: bool = False,
    ) -> DecryptedMessage:
        last_message = await self._storage.message.get_last_message(
            input_message.user_id
        )
        if last_message is not None:
            if last_message.sender == sender:
                raise LastMessageSenderRepeatsException()

        now = datetime.now()
        message = EncryptedMessage(
            encrypted_content=self._encryptor.encrypt(input_message.content),
            sender=sender,
            user_id=input_message.user_id,
            created_at=now,
        )

        message_id = await self._storage.message.create_message(message)
        if commit:
            await self._storage.commit()

        return DecryptedMessage(
            id=message_id,
            sender=sender,
            content=input_message.content,
            user_id=input_message.user_id,
            created_at=now,
        )

    async def create_user_message(
        self, input_message: InputMessage, commit: bool = False
    ) -> DecryptedMessage:
        return await self._create_message(
            input_message=input_message,
            sender=MessageSenderType.USER,
            commit=commit,
        )

    async def create_assistant_message(
        self, input_message: InputMessage, commit: bool = False
    ) -> DecryptedMessage:
        return await self._create_message(
            input_message=input_message,
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
