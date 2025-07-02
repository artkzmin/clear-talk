from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import timedelta

from src.application.services.user import get_telegram_user
from src.application.services.plan import get_plan_by_user_id

router = Router()


@router.message(Command("me"))
async def handle_me(msg: Message):
    user = await get_telegram_user(
        telegram_user_id=msg.from_user.id,
    )
    plan = await get_plan_by_user_id(
        user_id=user.id,
    )
    plan_expire_date = (
        plan.plan_activated_at + timedelta(days=plan.days_count)
        if plan.days_count
        else "Безлимит"
    )
    text = (
        "Твой профиль:"
        f"\n\nПлан: {plan.type_}"
        f"\nДата активации: {plan.plan_activated_at}"
        f"\nДата истечения: {plan_expire_date}"
    )
    await msg.answer(text)
