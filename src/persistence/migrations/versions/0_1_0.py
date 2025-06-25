"""0.1.0

Revision ID: a83f864c7ade
Revises:
Create Date: 2025-06-21 14:37:45.828238

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a83f864c7ade"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


plantype = sa.Enum("FREE", "PRO", "ADMIN", name="plantype")
externalservicetype = sa.Enum("TELEGRAM", name="externalservicetype")
messagesendertype = sa.Enum("USER", "ASSISTANT", name="messagesendertype")


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "plan",
        sa.Column(
            "type",
            plantype,
            server_default=sa.text("'FREE'"),
            nullable=False,
        ),
        sa.Column("days_count", sa.Integer(), nullable=True),
        sa.Column("max_messages_count", sa.Integer(), nullable=True),
        sa.Column("max_context_tokens", sa.Integer(), nullable=True),
        sa.Column("max_output_tokens", sa.Integer(), nullable=True),
        sa.Column(
            "id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.CheckConstraint(
            "(days_count IS NULL OR days_count >= 0) "
            "AND (max_messages_count IS NULL OR max_messages_count >= 0) "
            "AND (max_context_tokens IS NULL OR max_context_tokens >= 0) "
            "AND (max_output_tokens IS NULL OR max_output_tokens >= 0)",
            name="chk_positive_or_null_limits",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("type"),
    )
    op.create_table(
        "user",
        sa.Column("hashed_external_id", sa.String(length=64), nullable=False),
        sa.Column(
            "external_service",
            externalservicetype,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column(
            "plan_activated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["plan.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "external_service", "hashed_external_id", name="uq_user_service_id"
        ),
    )
    op.create_table(
        "message",
        sa.Column(
            "sender",
            messagesendertype,
            nullable=False,
        ),
        sa.Column("encrypted_content", sa.Text(), nullable=False),
        sa.Column("previous_message_id", sa.UUID(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.ForeignKeyConstraint(
            ["previous_message_id"],
            ["message.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("previous_message_id"),
    )

    # Create Plans
    op.execute(
        "INSERT INTO plan"
        "(type, days_count, max_messages_count, max_context_tokens, max_output_tokens)"
        "VALUES ('FREE', NULL, NULL, NULL, NULL)"
    )
    op.execute(
        "INSERT INTO plan"
        "(type, days_count, max_messages_count, max_context_tokens, max_output_tokens)"
        "VALUES ('PRO', NULL, NULL, NULL, NULL)"
    )
    op.execute(
        "INSERT INTO plan"
        "(type, days_count, max_messages_count, max_context_tokens, max_output_tokens)"
        "VALUES ('ADMIN', NULL, NULL, NULL, NULL)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("message")
    op.drop_table("user")
    op.drop_table("plan")

    plantype.drop(op.get_bind())
    externalservicetype.drop(op.get_bind())
    messagesendertype.drop(op.get_bind())
