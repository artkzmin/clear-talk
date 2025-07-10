from datetime import timedelta
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils import markdown

from src.application.services.user import get_telegram_user
from src.application.services.plan import get_remaining_user_plan

from src.presentation.bot.constants import (
    CommandsConstants,
    SymbolsConstants,
    EmojiConstants,
)
from src.presentation.bot import utils

router = Router()


@router.message(Command(CommandsConstants.ME.name))
async def handle_me(msg: Message):
    user = await get_telegram_user(
        telegram_user_id=msg.from_user.id,
    )
    remaining_user_plan = await get_remaining_user_plan(
        user_id=user.id,
    )

    plan_activated_at = utils.get_ru_format_date(
        remaining_user_plan.plan_activated_at,
    )

    plan_expire_date = (
        utils.get_ru_format_date(
            remaining_user_plan.plan_activated_at
            + timedelta(days=remaining_user_plan.days_count)
        )
        if remaining_user_plan.days_count
        else SymbolsConstants.INFINITY
    )
    remaining_messages_count = (
        remaining_user_plan.remaining_messages_count
        if remaining_user_plan.remaining_messages_count
        else SymbolsConstants.INFINITY
    )
    remaining_days_count = (
        remaining_user_plan.remaining_days_count
        if remaining_user_plan.remaining_days_count
        else SymbolsConstants.INFINITY
    )
    text = (
        f"{markdown.bold('Твой профиль')}"
        f"\n\n{markdown.bold(f'{EmojiConstants.ticket} Подписка')}: "
        f"{remaining_user_plan.type_}"
        f"\n{markdown.bold(f'{EmojiConstants.calendar} Дата активации')}: "
        f"{plan_activated_at}"
        f"\n{markdown.bold(f'{EmojiConstants.calendar} Дата истечения')}: "
        f"{plan_expire_date}"
        f"\n{markdown.bold(f'{EmojiConstants.message} Оставшиеся сообщения')}: "
        f"{remaining_messages_count}"
        f"\n{markdown.bold(f'{EmojiConstants.sandglass} Оставшиеся дни')}: "
        f"{remaining_days_count}"
    )
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN)
