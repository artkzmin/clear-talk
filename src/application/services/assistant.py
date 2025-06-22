from src.persistence.storage import inject_storage, Storage
from src.core.message.entities import InputMessage
from src.core.assistant.services import AssistantService

from src.infrastructure.clients.assistant import OpenAIAssistantClient
from src.infrastructure.utils.token import TiktokenTokenUtility
from src.infrastructure.utils.encryptor import FernetEncryptorUtility


@inject_storage
async def get_assistant_answer(message_input: InputMessage, storage: Storage) -> str:
    return await AssistantService(
        storage=storage,
        assistant_client=OpenAIAssistantClient(),
        token_utility=TiktokenTokenUtility(),
        encryptor=FernetEncryptorUtility(),
    ).get_assistant_answer(message_input)
