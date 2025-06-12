from pathlib import Path
from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

BASE_DIR: Path = Path(__file__).parent.parent
ENV_PATH: Path = BASE_DIR / "config" / ".env"


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


class APISettings(BaseModel):
    url: HttpUrl
    key: str


class AssistantSettings(BaseModel):
    model_name: str
    system_message: str
    api: APISettings


class Settings(BaseSettings):
    mode: Literal["TEST", "LOCAL", "DEV", "PROD"]

    db: DBSettings
    assistant: AssistantSettings

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
    )


settings = Settings()
