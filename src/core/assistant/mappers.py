from typing import Sequence
from src.core.message.entities import Message
from src.core.assistant.entities import AssistantChat, AssistantChatMessage


class AssistantChatMapper:
    @staticmethod
    def from_messages(messages: Sequence[Message]) -> AssistantChat:
        return AssistantChat(
            messages=[
                AssistantChatMessage(
                    content=message.content,
                    sender=message.sender_type,
                )
                for message in messages
            ]
        )
