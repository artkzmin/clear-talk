import os
from pathlib import Path
from enum import StrEnum
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Final
from dotenv import load_dotenv


CONFIG_FILE_NAME: Final = os.getenv("CLEAR_TALK_CONFIG", ".env")

BASE_DIR: Final = Path(__file__).parent.parent.parent
ENV_PATH: Final = BASE_DIR / "config" / CONFIG_FILE_NAME

load_dotenv(ENV_PATH, override=True)


class ModeType(StrEnum):
    TEST = "TEST"
    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"


class Settings(BaseSettings):
    class DBSettings(BaseModel):
        host: str
        port: int
        user: str
        password: str
        name: str

        @property
        def url(self) -> str:
            return (
                f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:"
                f"{self.port}/{self.name}"
            )

    class AssistantSettings(BaseModel):
        class AssistantModelSettings(BaseModel):
            name: str
            tokeniser: str
            temperature: float

        model: AssistantModelSettings
        system_message: str
        api_key: str

    class TelegramSettings(BaseModel):
        admin_id: int
        bot_token: str

    class LogsSettings(BaseModel):
        dir_path: Path

        @field_validator("dir_path", mode="before")
        def resolve_dir_path(cls, v: str | Path) -> Path:
            return Path(v).resolve()

    class SecuritySettings(BaseModel):
        hash_key: str
        encrypt_key: str

    mode: ModeType
    db: DBSettings
    assistant: AssistantSettings
    telegram: TelegramSettings
    logs: LogsSettings
    security: SecuritySettings

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
    )


settings = Settings()
