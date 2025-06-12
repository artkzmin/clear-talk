from src.core.message.entities import Message
from src.core.token.interfaces import TokenUtilityInterface


class TokenService:
    def __init__(self, token_utility: TokenUtilityInterface) -> None:
        self.token_utility = token_utility

    def get_tokens_count(self, messages: list[Message]) -> int:
        result = 0
        for message in messages:
            result += self.token_utility.get_tokens_count(message.content)
        return result
