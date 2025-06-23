from langchain_openai import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage,
    AIMessage,
)

from src.infrastructure.config import settings

from src.core.message.enums import MessageSenderType
from src.core.message.entities import DecryptedMessage
from src.core.assistant.interfaces import AssistantClientInterface
from src.core.assistant.exceptions import AssistantClientException


class OpenAIAssistantClient(AssistantClientInterface):
    def __init__(self):
        self._chat = ChatOpenAI(
            model_name=settings.assistant.model.name,
            openai_api_key=settings.assistant.api_key,
            temperature=settings.assistant.model.temperature,
        )

    async def get_chat_completion_answer(
        self, messages_chain: list[DecryptedMessage]
    ) -> str:
        lc_messages = self._convert_messages_chain_to_lc_messages(messages_chain)

        response = await self._chat.agenerate(messages=[lc_messages])
        return response.generations[0][0].text

    def _convert_messages_chain_to_lc_messages(
        self, messages_chain: list[DecryptedMessage]
    ) -> list[DecryptedMessage]:
        lc_messages = [SystemMessage(content=settings.assistant.system_message)]
        for msg in messages_chain:
            if msg.sender == MessageSenderType.USER:
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.sender == MessageSenderType.ASSISTANT:
                lc_messages.append(AIMessage(content=msg.content))
            elif msg.sender == MessageSenderType.SYSTEM:
                lc_messages.append(SystemMessage(content=msg.content))
            else:
                raise AssistantClientException()
        return lc_messages
