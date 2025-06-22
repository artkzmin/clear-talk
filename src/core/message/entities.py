from uuid import UUID
from datetime import datetime
from src.core.abc.entities import BaseEntityUUID, BaseEntity
from src.core.message.enums import MessageSenderType


class EncryptedMessage(BaseEntityUUID):
    sender: MessageSenderType
    encrypted_content: str
    previous_message_id: UUID | None = None
    user_id: UUID
    created_at: datetime


class DecryptedMessage(BaseEntityUUID):
    sender: MessageSenderType
    content: str
    previous_message_id: UUID | None = None
    user_id: UUID
    created_at: datetime


class InputMessage(BaseEntity):
    content: str
    user_id: UUID
