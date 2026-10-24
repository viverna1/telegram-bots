from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from core.root import chat_service
from core.shared.message_log import message_log

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Это scratch.")


@router.message()
async def message_handler(message: Message, bot: Bot):
    message_log(message, chat_service=chat_service)

    if message.text:
        await message.answer(message.text)


@router.business_message()
async def business_message_handler(message: Message):
    message_log(message, chat_service=chat_service)

    if message.text:
        await message.answer(message.text)
