from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message

from core.presentation.handlers import (
    base_message_handler,
    base_start,
)

router = Router()
START_TEXT = html.quote("""
!!принимаем с 14+ лет, от 40 лвла(можем делать исключения)!!
Заполните анкету по шаблону:
1.фото скина
(рофл скины,вешалки не берем)
2.фото лвла
3.ваш возраст
4.что умеете?
(деш,тримп,слайд и тд)
5.что вы будете делать когда в чате ссора между участниками?
6.ваш юз в тг
(без юза не берем)
7.состоите ли вы в каких то еще кланах?
(обязательно укажите в каком)
""")
START_TEXT = html.quote(f"{html.bold('123')}32")


@router.message(Command("start"))
async def cmd_start(message: Message):
    base_start(message)
    await message.answer(START_TEXT)


@router.message()
async def message_handler(message: Message):
    base_message_handler(message)
