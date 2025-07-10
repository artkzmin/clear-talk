from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown

from src.application.services.assistant import get_assistant_answer
from src.application.services.user import get_or_create_telegram_user
from src.application.services.plan import get_user_plan

from src.core.message.entities import InputMessage
from src.core.plan.enums import PlanType

from src.core.plan_checker.exceptions import (
    PlanNotActiveException,
    PlanMessagesCountLimitException,
    PlanTokensLimitException,
)
from src.presentation.bot.constants import CommandsConstants

router = Router()


@router.message(F.text)
async def handle_single(msg: Message):
    user = await get_or_create_telegram_user(
        telegram_user_id=msg.from_user.id,
    )
    try:
        answer = await get_assistant_answer(
            InputMessage(
                content=msg.text,
                user_id=user.id,
            )
        )
    except (
        PlanNotActiveException,
        PlanMessagesCountLimitException,
        PlanTokensLimitException,
    ) as e:
        if isinstance(e, PlanNotActiveException):
            answer = "План не активен"
        elif isinstance(e, PlanMessagesCountLimitException):
            answer = "Достигнут лимит сообщений"
        elif isinstance(e, PlanTokensLimitException):
            answer = "Достигнут лимит токенов"
        user_plan = await get_user_plan(
            user_id=user.id,
        )
        if user_plan.type_ == PlanType.FREE:
            answer += (
                f"\n\n{markdown.bold(f'/{CommandsConstants.PAY.name.lower()}')}"
                f" - {CommandsConstants.PAY.description}"
            )

    await msg.answer(answer, parse_mode=ParseMode.MARKDOWN)
