from core.presentation.bot import Bot

from .handlers import router

# from .handlers_clean import router


def main():
    bot = Bot(router)
    bot.run()


if __name__ == "__main__":
    main()
