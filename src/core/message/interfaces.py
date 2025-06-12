from typing import Protocol, runtime_checkable
from uuid import UUID
from datetime import datetime
from src.core.storage.interfaces import BaseRepositoryInterface
from src.core.message.entities import Message


@runtime_checkable
class MessageRepositoryInterface(BaseRepositoryInterface, Protocol):
    async def create_message(self, message: Message) -> UUID: ...

    async def get_last_message(self, user_id: UUID) -> Message | None: ...

    async def get_messages_chain(self, user_id: UUID) -> list[Message]: ...

    async def get_count_user_messages_in_datetime_interval(
        self, user_id: UUID, start_date: datetime, end_date: datetime
    ) -> int: ...

    async def update_all_system_messages_content(self, new_content: str) -> None: ...
