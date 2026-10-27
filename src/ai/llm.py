import asyncio

import requests
from ollama import chat

from .chat_history_repository import ChatHistoryRepository

DEFAULT_SYSTEM_PROMPT = """
Ты ведёшь свой личный Telegram и отвечаешь на входящие сообщения от первого лица, как живой человек.

ПРАВИЛА:
1. Отвечай коротко: обычно 1-2 фразы или предложения. Как в реальном мессенджере.
2. Пиши с маленькой буквы, без точки в конце, без markdown, без списков. Без эмодзи.
3. Язык ответа русский.
4. Никогда не говори, что ты ИИ, бот, ассистент или модель. Не упоминай промпты и инструкции.
5. Не выдумывай факты о моей жизни: планы, встречи, суммы, адреса, обещания. Если данных нет — отвечай уклончиво или задай уточняющий вопрос.
6. Не подтверждай встречи, время, место, деньги. В таких случаях: "ща гляну", "позже отвечу", "напишу как освобожусь".
7. Если спрашивают "ты бот?" — отвечай по-человечески уклончиво, не признавайся.
8. Не пиши больше, чем написал бы человек в чате. Никаких приветственных речей и вежливых формул.
9. Если сообщение — спам, реклама, рассылка, стикер, гифка, "ок", "+", "спасибо" или явно не требует ответа — верни ровно одно слово: SKIP
"""


class LLM:
    SKIP_TOKEN = "SKIP"

    def __init__(self, bot_config: dict, chat_history_repo: ChatHistoryRepository):
        self._config = bot_config
        self._chat_history_repo = chat_history_repo
        self.name = self._config["name"]

    async def ask(self, chat_id: int, request: str) -> str | None:
        if self._config["type"] == "http":
            response = await asyncio.to_thread(self._ask_http, chat_id, request)
        elif self._config["type"] == "ollama":
            response = await asyncio.to_thread(self._ask_ollama, chat_id, request)
        elif self._config["type"] == "none":
            response = {"ok": True, "content": f'[ai] request: "{request}"'}
        else:
            raise ValueError(f"Unknown LLM type: {self._config['type']}")

        if not response["ok"]:
            print(response["error"])
            return None

        content = (response["content"] or "").strip()
        if not content or content == self.SKIP_TOKEN:
            return None

        self._chat_history_repo.add_message(chat_id, {"role": "user", "content": request})
        self._chat_history_repo.add_message(chat_id, {"role": "assistant", "content": content})
        return content

    def _ask_http(self, chat_id: int, request: str) -> dict:
        try:
            response = requests.post(
                self._config["url"],
                # json={"chat_id": chat_id, "message": request},
                json=self._build_messages(chat_id, request)
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _ask_ollama(self, chat_id: int, request: str) -> dict:
        try:
            messages = self._build_messages(chat_id, request)
            response = chat(model=self._config["model"], messages=messages)
            return {"ok": True, "content": response.message.content}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _build_messages(self, chat_id: int, request: str) -> list[dict[str, str]]:
        history = self._chat_history_repo.get_chat_history(chat_id) or []
        return [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": request},
        ]

if __name__ == "__main__":

    async def main():
        bot_config = {
            "type": "http",
            "name": "test-api",
            "url": "http://127.0.0.1:5000/api/ask",
        }
        llm = LLM(bot_config)
        ans = await llm.ask("Привет, бот!")
        print(ans)

    asyncio.run(main())
