from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils import markdown
from src.presentation.bot.constants import CommandsConstants, EmojiConstants


router = Router()

commands = [
    value
    for value in CommandsConstants.__dict__.values()
    if isinstance(value, CommandsConstants.Command)
]


@router.message(Command("help"))
async def handle_help(msg: Message):
    text = f"{markdown.bold(f'{EmojiConstants.list_} Список команд')}\n\n"
    for cmd in commands:
        text += f"{markdown.bold(f'/{cmd.name.lower()}')} - {cmd.description}\n"
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN)
