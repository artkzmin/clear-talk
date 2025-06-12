from pydantic import BaseModel, model_validator
from src.core.message.enums import MessageSenderType
from src.core.message.entities import BaseMessageInput
from src.core.assistant.exceptions import (
    MessagesMustNotBeEmptyException,
    FirstMessageMustBeFromSystemException,
    InvalidSenderException,
)


class AssistantModel(BaseModel):
    model_name: str
    api_key: str


class AssistantChatMessage(BaseMessageInput):
    content: str
    sender: MessageSenderType

    async def as_str(self) -> str:
        return self.content


class AssistantChat(BaseModel):
    messages: list[AssistantChatMessage]

    @model_validator(mode="after")
    def validate_message_sequence(self) -> "AssistantChat":
        if not self.messages:
            raise MessagesMustNotBeEmptyException()

        if self.messages[0].sender != MessageSenderType.SYSTEM:
            raise FirstMessageMustBeFromSystemException()

        expected_sender = MessageSenderType.USER
        for message in self.messages[1:]:
            if message.sender != expected_sender:
                raise InvalidSenderException()
            expected_sender = (
                MessageSenderType.ASSISTANT
                if expected_sender == MessageSenderType.USER
                else MessageSenderType.USER
            )

        return self
