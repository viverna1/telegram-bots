import asyncio

from aiogram.enums import ParseMode

from core.presentation.bot import Bot

from .handlers import router


async def main():
    bot = Bot(router, parse_mode=ParseMode.HTML)
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
