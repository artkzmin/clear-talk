from abc import ABC, abstractmethod
from uuid import UUID
from pydantic import BaseModel
from src.core.abc.entities import BaseEntityUUID
from src.core.message.enums import MessageSenderType


class Message(BaseEntityUUID):
    sender_type: MessageSenderType
    content: str
    previous_message_id: UUID | None = None


class BaseMessageInput(BaseModel, ABC):
    @abstractmethod
    async def as_str(self) -> str:
        pass


class SingleMessageInput(BaseMessageInput):
    content: str

    async def as_str(self) -> str:
        return self.content


class DialogMessage(BaseModel):
    sender_name: str
    content: str


class DialogInput(BaseMessageInput):
    messages: list[DialogMessage]

    async def as_str(self) -> str:
        return "\n".join(
            f"{msg.sender.first_name}: {msg.content}" for msg in self.messages
        )
