from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

from src.application.services.assistant import get_assistant_answer
from src.application.services.user import get_or_create_telegram_user

from src.core.message.entities import InputMessage

from src.core.plan_checker.exceptions import (
    PlanNotActiveException,
    PlanMessagesCountLimitException,
    PlanTokensLimitException,
)

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
    except PlanNotActiveException:
        answer = "План не активен"
    except PlanMessagesCountLimitException:
        answer = "Достигнут лимит сообщений"
    except PlanTokensLimitException:
        answer = "Достигнут лимит токенов"
    await msg.answer(answer, parse_mode=ParseMode.MARKDOWN)
