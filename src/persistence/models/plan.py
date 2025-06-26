from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.core.plan.enums import PlanType

from src.infrastructure.db.base import BaseUUIDModel


class PlanModel(BaseUUIDModel):
    __tablename__ = "plan"

    type_: Mapped[PlanType] = mapped_column(
        "type",
        nullable=False,
        unique=True,
    )
    days_count: Mapped[int] = mapped_column(nullable=True)
    max_messages_count: Mapped[int] = mapped_column(nullable=True)
    max_context_tokens: Mapped[int] = mapped_column(nullable=True)
    max_output_tokens: Mapped[int] = mapped_column(nullable=True)

    __table_args__ = (
        CheckConstraint(
            "(days_count IS NULL OR days_count >= 0) AND "
            "(max_messages_count IS NULL OR max_messages_count >= 0) AND "
            "(max_context_tokens IS NULL OR max_context_tokens >= 0) AND "
            "(max_output_tokens IS NULL OR max_output_tokens >= 0)",
            name="chk_positive_or_null_limits",
        ),
    )
