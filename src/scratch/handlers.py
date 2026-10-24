from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from core.presentation.handlers import base_start
from core.shared.message_log import log

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await base_start(message)
    print("start")
    await message.answer("Привет! Это scratch.")


@router.message()
async def echo(message: types.Message):
    if message.text is None: return
    log(message)
    await message.answer(message.text)

@router.message_reaction()
async def message_reaction_handler(message_reaction: types.MessageReactionUpdated):
    print(message_reaction)

@router.business_connection()
async def business_connection_handler(business_connection: types.BusinessConnection):
    print("business_connection")
    print(business_connection)

@router.business_message()
async def business_message_handler(message: Message):
    log(message)