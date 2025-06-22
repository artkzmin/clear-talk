from aiogram import Router
from src.presentation.bot.handlers import start, help, text_message


def get_main_router() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(help.router)
    router.include_router(text_message.router)

    return router
