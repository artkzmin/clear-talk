from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def handle_help(msg: Message):
    await msg.answer("Привет, я бот — ИИ-помощник")
