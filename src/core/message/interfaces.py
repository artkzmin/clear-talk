from typing import Protocol, runtime_checkable, ClassVar
from uuid import UUID
from datetime import date
from src.core.abc.interfaces import BaseRepositoryInterface
from src.core.message.entities import EncryptedMessage


@runtime_checkable
class MessageRepositoryInterface(BaseRepositoryInterface, Protocol):
    async def create_message(self, message: EncryptedMessage) -> UUID: ...

    async def get_last_message(self, user_id: UUID) -> EncryptedMessage | None: ...

    async def get_messages_chain(self, user_id: UUID) -> list[EncryptedMessage]: ...

    async def get_count_user_messages_in_date_interval(
        self, user_id: UUID, start_date: date, end_date: date
    ) -> int: ...


@runtime_checkable
class MessageParametersInterface(Protocol):
    SYSTEM_MESSAGE_CONTENT: ClassVar[str]
