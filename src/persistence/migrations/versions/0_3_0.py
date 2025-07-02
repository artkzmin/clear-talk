"""0_3_0

Revision ID: f1f3fbac5843
Revises: e225efc3cea6
Create Date: 2025-06-29 18:41:30.953929

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f1f3fbac5843"
down_revision: Union[str, None] = "e225efc3cea6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "user",
        "plan_activated_at",
        existing_type=postgresql.DATE(),
        type_=sa.Date(),
        existing_nullable=True,
        existing_server_default=sa.text("now()"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "user",
        "plan_activated_at",
        existing_type=sa.Date(),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        existing_server_default=sa.text("now()"),
    )
