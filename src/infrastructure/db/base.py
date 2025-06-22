from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from src.core.constants import STR_ID_LENGTH


class BaseModel(DeclarativeBase):
    __abstract__ = True


class BaseUUIDModel(BaseModel):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )


class BaseStrIdModel(BaseModel):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(STR_ID_LENGTH),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )


class BaseIntIdModel(BaseModel):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
