import os
from pathlib import Path
from pydantic import BaseModel, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Final
from dotenv import load_dotenv
from src.infrastructure.config.enums import ModeType, ServiceType

CONFIG_FILE_NAME: Final = os.getenv("CLEAR_TALK_CONFIG", ".env")

BASE_DIR: Final = Path(__file__).parent.parent.parent.parent
CONFIG_DIR: Final = BASE_DIR / "config"

ENV_PATH: Final = CONFIG_DIR / CONFIG_FILE_NAME

SYSTEM_MESSAGE_FILE_NAME: Final = "system_message.conf"
SYSTEM_MESSAGE_PATH: Final = CONFIG_DIR / SYSTEM_MESSAGE_FILE_NAME

load_dotenv(ENV_PATH, override=True)


def load_system_message() -> str:
    return SYSTEM_MESSAGE_PATH.read_text(encoding="utf-8")


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
        system_message: str = Field(default_factory=load_system_message)
        api_key: str
        use_proxy: bool

    class TelegramSettings(BaseModel):
        admin_id: int
        bot_token: str

    class LogsSettings(BaseModel):
        dir_path: Path
        max_log_files: int

        @field_validator("dir_path", mode="before")
        def resolve_dir_path(cls, v: str | Path) -> Path:
            return Path(v).resolve()

    class SecuritySettings(BaseModel):
        hash_key: str
        encrypt_key: str

    class ProxySettings(BaseModel):
        host: str
        port: int
        user: str
        password: str

        def is_configured(self) -> bool:
            return all([self.host, self.port, self.user, self.password])

        @property
        def socks5(self) -> str | None:
            if not self.is_configured():
                return None
            return f"socks5://{self.user}:{self.password}@{self.host}:{self.port}"

    mode: ModeType
    service: ServiceType
    db: DBSettings
    assistant: AssistantSettings
    telegram: TelegramSettings
    logs: LogsSettings
    security: SecuritySettings
    proxy: ProxySettings

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
    )


settings = Settings()
