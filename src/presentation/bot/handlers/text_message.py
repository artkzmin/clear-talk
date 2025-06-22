from aiogram import Router, F
from aiogram.types import Message

from src.application.services.assistant import get_assistant_answer
from src.application.services.user import get_or_create_telegram_user

from src.core.message.entities import InputMessage

router = Router()


@router.message(F.text)
async def handle_single(msg: Message):
    user = await get_or_create_telegram_user(
        telegram_user_id=msg.from_user.id,
    )
    answer = await get_assistant_answer(
        InputMessage(
            content=msg.text,
            user_id=user.id,
        )
    )
    await msg.answer(answer)
