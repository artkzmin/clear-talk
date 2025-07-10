from aiogram import Router
from src.presentation.bot.handlers import text_message
from src.presentation.bot.routers.commands import get_commands_router


def get_main_router() -> Router:
    router = Router()

    router.include_router(get_commands_router())
    router.include_router(text_message.router)

    return router


__all__ = ["get_main_router"]
