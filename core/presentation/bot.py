import asyncio
import os
from typing import Callable

from aiogram import Bot as AiogramBot
from aiogram import Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv


class Bot:
    def __init__(self, router: Router, token: str | None = None, on_shutdown: list[Callable] | None = None, **workflow_data):
        load_dotenv()
        token = token or os.getenv("BOT_TOKEN")
        if not token:
            raise RuntimeError("BOT_TOKEN не задан")

        self._bot = AiogramBot(
            token=token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self._dp = Dispatcher()
        self._dp.include_router(router)
        if on_shutdown:
            for call in on_shutdown:
                self._dp.shutdown.register(call)
        self._dp.workflow_data.update(workflow_data)

    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        await self._bot.delete_webhook(drop_pending_updates=True)
        try:
            await self._dp.start_polling(self._bot)
        finally:
            await self._bot.session.close()
