from aiogram import Bot, Router
from aiogram.types import Message

from core.root import user_service

from .utils.aio_to_user import aio_to_user

router = Router()


@router.startup()
async def on_startup(bot: Bot):
    await bot.send_message(1400768976, "Bot started")


async def base_start(message: Message):
    user = message.from_user
    if user is not None:
        app_user = aio_to_user(user)
        
        if app_user is not None:
            user_service.create_user(app_user)
            
    await message.answer(
        "Ваше сообщение не отправлено, для отправки сообщения напишите /burmalda"
    )
