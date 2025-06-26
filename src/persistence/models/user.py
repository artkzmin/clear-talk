from datetime import datetime
from sqlalchemy import String, UniqueConstraint, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


from src.core.constants import STR_HASH_LENGTH
from src.core.user.enums import ExternalServiceType

from src.infrastructure.db.base import BaseUUIDModel


class UserModel(BaseUUIDModel):
    __tablename__ = "user"

    hashed_external_id: Mapped[str] = mapped_column(
        String(STR_HASH_LENGTH), nullable=False
    )
    external_service: Mapped[ExternalServiceType] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("now()")
    )
    plan_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("plan.id", ondelete="SET NULL"), nullable=True
    )
    plan_activated_at: Mapped[datetime] = mapped_column(
        nullable=True, server_default=text("now()")
    )

    __table_args__ = (
        UniqueConstraint(
            "external_service", "hashed_external_id", name="uq_user_service_id"
        ),
    )
