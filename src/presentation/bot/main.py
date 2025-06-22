import asyncio
from aiogram import Bot, Dispatcher
from src.infrastructure.config import settings
from src.infrastructure.logger import logger_app, setup_logging
from src.presentation.bot.routers.main_router import get_main_router
from src.presentation.bot.middlewares.only_admin import OnlyAdminMiddleware

setup_logging()
logger = logger_app.getChild(__name__)


async def main() -> None:
    logger.info("Starting bot...")
    bot = Bot(token=settings.telegram.bot_token)
    dp = Dispatcher()

    dp.include_router(get_main_router())
    dp.message.middleware(OnlyAdminMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
