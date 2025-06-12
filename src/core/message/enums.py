from enum import StrEnum


class MessageSenderType(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
