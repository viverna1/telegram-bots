from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.presentation.handlers import (
    base_business_message_handler,
    base_message_handler,
    base_start,
)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    base_start(message)
    await message.answer("Привет! Это scratch.")


@router.message()
async def message_handler(message: Message):
    base_message_handler(message)

    if message.text:
        await message.answer(f"[{message.text}]")


@router.business_message()
async def business_message_handler(message: Message):
    base_business_message_handler(message)
    
    if message.text:
        await message.answer(f"[{message.text}]")


@router.channel_post()
async def channel_post_handler(channel_post: Message):
    base_message_handler(channel_post)

    if channel_post.text:
        await channel_post.answer(f"[{channel_post.text}]")