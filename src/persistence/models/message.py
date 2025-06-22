from datetime import datetime
from sqlalchemy import ForeignKey, Text, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


from src.core.message.enums import MessageSenderType

from src.infrastructure.db.base import BaseUUIDModel


class MessageModel(BaseUUIDModel):
    __tablename__ = "message"

    sender: Mapped[MessageSenderType] = mapped_column(nullable=False)
    encrypted_content: Mapped[str] = mapped_column(Text, nullable=False)
    previous_message_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("message.id"), nullable=True, unique=True
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("now()")
    )
