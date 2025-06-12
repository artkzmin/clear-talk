from typing import Protocol, runtime_checkable
from src.core.assistant.entities import AssistantChat, AssistantModel


@runtime_checkable
class AssistantClientInterface(Protocol):
    assistant_model: AssistantModel

    def __init__(self, assistant_model: AssistantModel) -> None: ...

    async def get_chat_completion_answer_content(self, chat: AssistantChat) -> str: ...
