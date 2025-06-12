from typing import Protocol, runtime_checkable


@runtime_checkable
class TokenUtilityInterface(Protocol):
    def get_tokens_count(self, string: str) -> int: ...
