from src.core.message.services import MessageService
from src.core.message.entities import InputMessage
from src.core.assistant.interfaces import (
    AssistantClientInterface,
    TokenUtilityInterface,
)
from src.core.assistant.exceptions import AssistantClientException
from src.core.interfaces import StorageInterface, EncryptorUtilityInterface


class AssistantService:
    def __init__(
        self,
        storage: StorageInterface,
        assistant_client: AssistantClientInterface,
        token_utility: TokenUtilityInterface,
        encryptor: EncryptorUtilityInterface,
    ) -> None:
        self._storage = storage
        self._message_service = MessageService(storage=storage, encryptor=encryptor)
        self._assistant_client = assistant_client
        self._token_utility = token_utility

    async def get_assistant_answer(self, user_message: InputMessage) -> str:
        await self._message_service.create_user_message(user_message)

        messages_chain = await self._message_service.get_messages_chain(
            user_message.user_id
        )
        try:
            assistant_answer = await self._assistant_client.get_chat_completion_answer(
                messages_chain
            )
        except AssistantClientException as e:
            raise e
        await self._message_service.create_assistant_message(
            InputMessage(
                content=assistant_answer,
                user_id=user_message.user_id,
            )
        )
        await self._storage.commit()
        return assistant_answer
