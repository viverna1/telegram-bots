import asyncio

from core.presentation.bot import Bot

from .handlers import router

# from .handlers_clean import router


async def main():
    bot = Bot(router)
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
