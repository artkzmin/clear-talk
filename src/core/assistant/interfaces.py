from typing import Optional, Protocol, runtime_checkable
from src.core.message.entities import DecryptedMessage


@runtime_checkable
class AssistantClientInterface(Protocol):
    async def get_chat_completion_answer(
        self,
        messages_chain: list[DecryptedMessage],
        max_output_tokens: Optional[int],
    ) -> str:
        """
        Raises:
        src.core.assistant.exceptions.AssistantClientException:
            If the assistant client fails to generate a response.
        """
