import tiktoken

from src.infrastructure.config import settings

from src.core.plan_checker.interfaces import TokenUtilityInterface


class TiktokenTokenUtility(TokenUtilityInterface):
    def __init__(self):
        self._encoder = tiktoken.get_encoding(settings.assistant.model.tokeniser)

    def get_tokens_count(self, string: str) -> int:
        tokens = self._encoder.encode(string)
        return len(tokens)
