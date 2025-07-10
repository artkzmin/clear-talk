from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils import markdown

from src.infrastructure.config import settings, ModeType
from src.infrastructure.logger import logger_app
from src.infrastructure.utils.hasher import HmacSha256Hasher

logger = logger_app.getChild(__name__)


class OnlyAdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if (
            settings.mode == ModeType.LOCAL
            and event.from_user.id != settings.telegram.admin_id
        ):
            await event.answer(
                f"❌ {markdown.bold('Извините, доступ запрещён')}"
                f"\n\nВаш ID в Telegram: {markdown.code(event.from_user.id)}",
                parse_mode=ParseMode.MARKDOWN,
            )
            logger.info(
                "Access denied for user %s",
                HmacSha256Hasher().get_hash(str(event.from_user.id)),
            )
            return None
        return await handler(event, data)
