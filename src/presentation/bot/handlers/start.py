from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.application.services.user import get_or_create_telegram_user

router = Router()


@router.message(Command("start"))
async def handle_start(msg: Message):
    user = await get_or_create_telegram_user(
        telegram_user_id=msg.from_user.id,
    )
    await msg.answer(
        f"Привет, я бот — ИИ-помощник."
        f"\n\nВаш ID: {user.id}"
        f"\n\nВаш ID в Telegram: {msg.from_user.id}"
    )
