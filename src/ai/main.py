import json
from pathlib import Path

from core.presentation.bot import Bot

from .handlers import router
from .llm import LLM

CONFIG_PATH = Path(__file__).parent / "config.json"


def choose_llm(config):
    print("\n".join(f"{i + 1}: {llm['name']}" for i, llm in enumerate(config)))
    answer = int(input(">>> ")) - 1
    return config[answer]


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
        llm_config = config[0] # choose_llm(config)

    llm = LLM(llm_config)
    bot = Bot(router, llm=llm)
    bot.run()


if __name__ == "__main__":
    main()
