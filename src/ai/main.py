import json
from pathlib import Path

from core.infrastructure.json_repository import JsonRepository
from core.presentation.bot import Bot

from .chat_history_repository import ChatHistoryRepository
from .handlers import router
from .llm import LLM

DATA_PATH = Path(__file__).parent / "data" / "chat_history.json"
MODELS_CONFIG_PATH = Path(__file__).parent / "models.json"


def choose_llm(models):
    print("\n".join(f"{i + 1}: {llm['name']}" for i, llm in enumerate(models)))
    answer = int(input(">>> ")) - 1
    return models[answer]


def main():
    with open(MODELS_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
        llm_config = choose_llm(config)

    json_repo = JsonRepository(str(DATA_PATH))
    chat_history_repository = ChatHistoryRepository(json_repo)

    llm = LLM(llm_config, chat_history_repository)
    bot = Bot(router, llm=llm)
    bot.run()


if __name__ == "__main__":
    main()
