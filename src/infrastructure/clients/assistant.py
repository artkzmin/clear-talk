from src.core.assistant.entities import AssistantChat, AssistantModel


class AssistantClient:
    def __init__(self, assistant_model: AssistantModel):
        self.assistant_model = assistant_model

    async def get_chat_completion_answer_content(self, chat: AssistantChat) -> str:
        pass
