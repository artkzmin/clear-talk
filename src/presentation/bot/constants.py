from typing import Final
from dataclasses import dataclass

from src.core.plan.enums import PlanType


class SymbolsConstants:
    INFINITY: Final = "∞"


class EmojiConstants:
    error: Final = "❌"
    success: Final = "✅"
    hello: Final = "👋"
    money: Final = "💰"
    info: Final = "ℹ️"
    list_: Final = "📋"
    message: Final = "💬"
    calendar: Final = "📅"
    ticket: Final = "🏷️"
    sandglass: Final = "⏳"


class CommandsConstants:
    @dataclass(frozen=True, slots=True)
    class Command:
        name: str
        description: str

    ME = Command("me", f"{EmojiConstants.info} информация о текущей подписке")
    PAY = Command("pay", f"{EmojiConstants.money} оплата подписки {PlanType.PRO}")
    PRO = Command("pro", f"{EmojiConstants.list_} информация о подписке {PlanType.PRO}")
