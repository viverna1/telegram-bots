from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from core.presentation.handlers import base_start
from core.shared.message_log import log

from .llm import LLM

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await base_start(message)


@router.message()
async def ask(message: types.Message, llm: LLM):
    if message.text is None:
        return
    log(message)

    answer = await llm.ask(message.text)
    print(f"[bot] -> [{message.from_user.username}]: {answer}")
    
    if answer is None or answer == LLM.SKIP_TOKEN:
        return

    await message.answer(answer)


@router.business_message()
async def business_message_handler(message: Message, llm: LLM):
    if message.text is None or message.from_user is None:
        return
    log(message)

    print(message)

    if message.from_user.id != message.chat.id:
        return

    answer = await llm.ask(message.text)
    log(message, sender=llm.name)
    
    if answer is None or answer == LLM.SKIP_TOKEN:
        return

    await message.answer(answer)

    