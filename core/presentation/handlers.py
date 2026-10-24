from aiogram import Bot, Router
from aiogram.types import Message

from core.root import chat_service, user_service
from core.shared.message_log import message_log

from .utils.aio_to_chat import aio_to_chat
from .utils.aio_to_user import aio_to_user

router = Router()


@router.startup()
async def on_startup(bot: Bot):
    await bot.send_message(1400768976, "Bot started")


def base_start(message: Message):
    user = message.from_user
    if user is not None:
        app_user = aio_to_user(user)

        if app_user is not None:
            user_service.create_user(app_user)


def base_message_handler(message: Message):
    chat = aio_to_chat(message)
    chat_service.upsert_chat_users(chat)

    message_log(message, chat_service=chat_service)


def base_business_message_handler(message: Message):
    chat = aio_to_chat(message)
    chat_service.upsert_chat_users(chat)

    message_log(message, chat_service=chat_service)
