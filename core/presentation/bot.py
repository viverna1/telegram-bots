import asyncio
import os

from aiogram import Bot as AiogramBot
from aiogram import Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv


class Bot:
    def __init__(self, router: Router, token: str | None = None, **workflow_data):
        load_dotenv()
        token = token or os.getenv("BOT_TOKEN")
        if not token:
            raise RuntimeError("BOT_TOKEN не задан")

        self._bot = AiogramBot(
            token=token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self._dispatcher = Dispatcher()
        self._dispatcher.include_router(router)
        self._dispatcher.workflow_data.update(workflow_data)

    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        await self._bot.delete_webhook(drop_pending_updates=True)
        await self._dispatcher.start_polling(self._bot)
