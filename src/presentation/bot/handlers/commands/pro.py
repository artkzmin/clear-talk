from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils import markdown
from src.presentation.bot.constants import CommandsConstants, EmojiConstants
from src.application.services.plan import get_pro_plan
from src.core.plan.enums import PlanType

router = Router()


@router.message(Command(CommandsConstants.PRO.name))
async def handle_subscriptions(msg: Message):
    pro = await get_pro_plan()
    text = (
        f"{EmojiConstants.ticket} "
        f"{markdown.bold(f'Возможности подписки {PlanType.PRO}')}"
        f"\n\n{markdown.bold(f'{EmojiConstants.sandglass} Количество дней')}: "
        f"{pro.days_count}"
        f"\n{markdown.bold(f'{EmojiConstants.message} Количество сообщений')}: "
        f"{pro.max_messages_count}"
    )
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN)
