"""0_2_1

Revision ID: e225efc3cea6
Revises: 1ed6f9c01927
Create Date: 2025-06-28 00:34:35.868626

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e225efc3cea6"
down_revision: Union[str, None] = "1ed6f9c01927"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("message_previous_message_id_key"), "message", type_="unique"
    )
    op.drop_constraint(
        op.f("message_previous_message_id_fkey"), "message", type_="foreignkey"
    )
    op.drop_column("message", "previous_message_id")

    op.execute("UPDATE plan SET max_output_tokens = 4000")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE plan SET max_output_tokens = NULL")

    op.add_column(
        "message",
        sa.Column(
            "previous_message_id",
            sa.UUID(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.create_foreign_key(
        op.f("message_previous_message_id_fkey"),
        "message",
        "message",
        ["previous_message_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint(
        op.f("message_previous_message_id_key"),
        "message",
        ["previous_message_id"],
        postgresql_nulls_not_distinct=False,
    )
