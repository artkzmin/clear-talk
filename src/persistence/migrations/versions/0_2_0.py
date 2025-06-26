"""0_2_0

Revision ID: 1ed6f9c01927
Revises: a83f864c7ade
Create Date: 2025-06-26 18:35:54.423032

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "1ed6f9c01927"
down_revision: Union[str, None] = "a83f864c7ade"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "UPDATE plan "
        "SET days_count = NULL, max_messages_count = 3, "
        "max_context_tokens = NULL, max_output_tokens = NULL "
        "WHERE type = 'FREE'"
    )
    op.execute(
        "UPDATE plan "
        "SET days_count = 30, max_messages_count = 100, "
        "max_context_tokens = NULL, max_output_tokens = NULL "
        "WHERE type = 'PRO'"
    )
    op.execute(
        "UPDATE plan "
        "SET days_count = NULL, max_messages_count = NULL, "
        "max_context_tokens = NULL, max_output_tokens = NULL "
        "WHERE type = 'ADMIN'"
    )

    op.drop_constraint(op.f("message_user_id_fkey"), "message", type_="foreignkey")
    op.drop_constraint(
        op.f("message_previous_message_id_fkey"), "message", type_="foreignkey"
    )
    op.create_foreign_key(
        "message_user_id_fkey",
        "message",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "message_previous_message_id_fkey",
        "message",
        "message",
        ["previous_message_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(op.f("user_plan_id_fkey"), "user", type_="foreignkey")
    op.create_foreign_key(
        "user_plan_id_fkey", "user", "plan", ["plan_id"], ["id"], ondelete="SET NULL"
    )

    op.alter_column("user", "plan_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column(
        "user",
        "plan_activated_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "user",
        "plan_activated_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column("user", "plan_id", existing_type=sa.UUID(), nullable=False)

    op.drop_constraint("user_plan_id_fkey", "user", type_="foreignkey")
    op.create_foreign_key(
        op.f("user_plan_id_fkey"), "user", "plan", ["plan_id"], ["id"]
    )
    op.drop_constraint(
        "message_previous_message_id_fkey", "message", type_="foreignkey"
    )
    op.drop_constraint("message_user_id_fkey", "message", type_="foreignkey")
    op.create_foreign_key(
        op.f("message_previous_message_id_fkey"),
        "message",
        "message",
        ["previous_message_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("message_user_id_fkey"), "message", "user", ["user_id"], ["id"]
    )

    op.execute(
        "UPDATE plan "
        "SET days_count = NULL, max_messages_count = NULL, "
        "max_context_tokens = NULL, max_output_tokens = NULL "
        "WHERE type = 'FREE'"
    )
    op.execute(
        "UPDATE plan "
        "SET days_count = NULL, max_messages_count = NULL, "
        "max_context_tokens = NULL, max_output_tokens = NULL "
        "WHERE type = 'PRO'"
    )
    op.execute(
        "UPDATE plan "
        "SET days_count = NULL, max_messages_count = NULL, "
        "max_context_tokens = NULL, max_output_tokens = NULL "
        "WHERE type = 'ADMIN'"
    )
