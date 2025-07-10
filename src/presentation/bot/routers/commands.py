from aiogram import Router
from src.presentation.bot.handlers.commands import start, help, me, pay, pro


def get_commands_router() -> Router:
    router = Router()

    router.include_router(start.router)
    router.include_router(help.router)
    router.include_router(me.router)
    router.include_router(pay.router)
    router.include_router(pro.router)

    return router
