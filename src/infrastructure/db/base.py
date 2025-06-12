from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
from uuid import UUID, uuid4
from src.core.constants import STR_ID_LENGTH


class BaseOrm(DeclarativeBase):
    pass


class BaseUUIDOrm(BaseOrm):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )


class BaseStrIdOrm(BaseOrm):
    id: Mapped[str] = mapped_column(
        String(STR_ID_LENGTH),
        primary_key=True,
        default=lambda: str(uuid4()),
    )


class BaseIntIdOrm(BaseOrm):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
