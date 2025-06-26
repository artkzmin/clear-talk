from src.persistence.storage import inject_storage, Storage
from src.core.message.entities import InputMessage
from src.core.assistant.services import AssistantService
from src.core.plan_checker.service import PlanCheckerService
from src.infrastructure.clients.assistant import OpenAIAssistantClient
from src.infrastructure.utils.token import TiktokenTokenUtility
from src.infrastructure.utils.encryptor import FernetEncryptorUtility
from src.infrastructure.utils.hasher import HmacSha256Hasher


@inject_storage
async def get_assistant_answer(message_input: InputMessage, storage: Storage) -> str:
    """
    Raises:
        src.core.plan_checker.exceptions.PlanNotActiveException:
            If the plan is not active.
        src.core.plan_checker.exceptions.PlanMessagesCountLimitException:
            If the plan has reached the maximum number of messages.
        src.core.plan_checker.exceptions.PlanTokensLimitException:
            If the plan has reached the maximum number of tokens.
    """
    await PlanCheckerService(
        storage=storage,
        encryptor_utility=FernetEncryptorUtility(),
        token_utility=TiktokenTokenUtility(),
        hasher_utility=HmacSha256Hasher(),
    ).check_plan_for_new_message(message_input=message_input)

    return await AssistantService(
        storage=storage,
        assistant_client=OpenAIAssistantClient(),
        encryptor_utility=FernetEncryptorUtility(),
    ).get_assistant_answer(message_input)
