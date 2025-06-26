from src.core.message.services import MessageService
from src.core.message.entities import InputMessage
from src.core.assistant.interfaces import AssistantClientInterface
from src.core.assistant.exceptions import AssistantClientException
from src.core.interfaces import StorageInterface, EncryptorUtilityInterface
from src.core.plan.services import PlanService


class AssistantService:
    def __init__(
        self,
        storage: StorageInterface,
        assistant_client: AssistantClientInterface,
        encryptor_utility: EncryptorUtilityInterface,
    ) -> None:
        self._storage = storage
        self._message_service = MessageService(
            storage=storage, encryptor=encryptor_utility
        )
        self._assistant_client = assistant_client
        self._plan_service = PlanService(storage=storage)

    async def get_assistant_answer(self, user_message: InputMessage) -> str:
        user_plan = await self._plan_service.get_user_plan_by_user_id(
            user_message.user_id
        )

        await self._message_service.create_user_message(user_message)

        messages_chain = await self._message_service.get_messages_chain(
            user_message.user_id
        )
        try:
            assistant_answer = await self._assistant_client.get_chat_completion_answer(
                messages_chain,
                max_output_tokens=user_plan.max_output_tokens,
            )
        except AssistantClientException as e:
            await self._message_service.create_assistant_message(
                InputMessage(
                    content="",
                    user_id=user_message.user_id,
                )
            )
            raise e
        await self._message_service.create_assistant_message(
            InputMessage(
                content=assistant_answer,
                user_id=user_message.user_id,
            )
        )
        await self._storage.commit()
        return assistant_answer
