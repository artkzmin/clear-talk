from aiogram import Router
from aiogram.types import Message, LabeledPrice
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils import markdown

from src.infrastructure.config import settings
from src.presentation.bot.constants import CommandsConstants, EmojiConstants
from src.core.plan.enums import PlanType
from src.application.services.plan import get_user_plan_by_telegram_user_id

router = Router()


@router.message(Command(CommandsConstants.PAY.name))
async def handle_pay(message: Message):
    user_plan = await get_user_plan_by_telegram_user_id(
        telegram_user_id=message.from_user.id,
    )
    if user_plan.type_ == PlanType.PRO:
        text = (
            f"{EmojiConstants.error} Подписка {PlanType.PRO} уже активна"
            f"\n\n {markdown.bold(f'/{CommandsConstants.ME.name.lower()}')}"
            f" - {CommandsConstants.ME.description}"
        )
        await message.answer(text, parse_mode=ParseMode.MARKDOWN)
        return
    await message.answer_invoice(
        title=f"Оплата подписки {PlanType.PRO}",
        description=f"{EmojiConstants.money} Совершите платеж",
        payload="pay-pro-subscription",
        provider_token=settings.telegram.payment_provider_token,
        currency="RUB",
        prices=[
            LabeledPrice(
                label=f"{EmojiConstants.money} Оплата подписки {PlanType.PRO}",
                amount=19900,
            ),
        ],
        start_parameter="pay-pro-subscription",
    )
