from uuid import UUID
from src.core.message.services import MessageService, T
from src.core.assistant.mappers import AssistantChatMapper
from src.core.assistant.interfaces import AssistantClientInterface
from src.core.assistant.entities import AssistantModel, AssistantChatMessage
from src.core.message.enums import MessageSenderType
from src.core.plan.services import PlanService, UserPlanService
from src.core.assistant.exceptions import AssistantClientException
from src.core.token.services import TokenService
from src.core.storage.service import StorageService


class AssistantService:
    def __init__(
        self,
        storage: StorageService,
        message_service: type[MessageService],
        user_plan_service: type[UserPlanService],
        plan_service: type[PlanService],
        assistant_client: type[AssistantClientInterface],
        token_service: type[TokenService],
        assistant_model: AssistantModel,
    ) -> None:
        self.storage = storage
        self.message_service = message_service(storage)
        self.user_plan_service = user_plan_service(
            storage=storage,
            message_service=message_service,
            plan_service=plan_service,
            token_service=token_service,
        )
        self.assistant_client = assistant_client(assistant_model=assistant_model)

    async def get_assistant_answer(
        self, message_input: T, user_id: UUID
    ) -> AssistantChatMessage:
        await self.user_plan_service.check_user_plan(user_id)
        await self.message_service.add_user_message(message_input, user_id)
        messages = await self.message_service.get_messages_chain(user_id)
        assitant_chat = AssistantChatMapper.from_messages(messages)
        try:
            assistant_completion_content = (
                await self.assistant_client.get_chat_completion_answer_content(
                    assitant_chat
                )
            )
        except AssistantClientException as e:
            raise e
        assistant_message = AssistantChatMessage(
            content=assistant_completion_content,
            sender=MessageSenderType.ASSISTANT,
        )
        await self.message_service.add_assistant_message(
            assistant_message,
            user_id,
        )
        await self.storage.commit()
        return assistant_message
