from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from src.application.services.user import get_or_create_telegram_user
from src.presentation.bot.constants import EmojiConstants

router = Router()


@router.message(CommandStart())
async def handle_start(msg: Message):
    await get_or_create_telegram_user(
        telegram_user_id=msg.from_user.id,
    )
    text = (
        f"{EmojiConstants.hello} {markdown.bold('Привет')}!"
        "\n\nЯ психологический помощник на базе ИИ. "
        "Помогаю разобраться в переживаниях и "
        "предлагаю советы для улучшения настроения и общения"
        f"\n\n{EmojiConstants.list_} Список доступных команд: {markdown.bold('/help')}"
        f"\n\n{EmojiConstants.message} Отправь сообщение, чтобы начать диалог"
    )
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN)
