import os
from pathlib import Path
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from dotenv import load_dotenv


config_file_name = os.getenv("CLEAR_TALK_CONFIG", ".env")

BASE_DIR: Path = Path(__file__).parent.parent.parent
ENV_PATH: Path = BASE_DIR / "config" / config_file_name

load_dotenv(ENV_PATH, override=True)


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


class Settings(BaseSettings):
    mode: Literal["TEST", "LOCAL", "DEV", "PROD"]

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
