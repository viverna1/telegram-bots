import json
import logging
import queue
import threading
import urllib.request

import telebot
import requests


class Config:
    def __init__(self):
        with open("G:\\Git\\Scripts\\secretary tg bot\\config.json", "r", encoding="utf-8") as f:
            env = json.load(f)

        self.bot_token: str = env.get("TELEGRAM_BOT_TOKEN", "")
        self.pollinations_url: str = env.get(
            "POLLINATIONS_URL", "https://text.pollinations.ai/openai"
        )
        self.model: str = env.get("POLLINATIONS_MODEL", "openai")
        self.temperature: float = float(env.get("LLM_TEMPERATURE", "0.85"))
        self.max_tokens: int = int(env.get("LLM_MAX_TOKENS", "150"))
        self.request_timeout: int = int(env.get("LLM_TIMEOUT", "60"))
        self.queue_maxsize: int = int(env.get("LLM_QUEUE_MAXSIZE", "2"))

        self.system_prompt: str = env.get("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)

        if not self.bot_token:
            raise RuntimeError(
                "TELEGRAM_BOT_TOKEN is not set. Export it as an environment "
                "variable instead of hardcoding it in source."
            )


DEFAULT_SYSTEM_PROMPT = """
Ты ведёшь свой личный Telegram и отвечаешь на входящие сообщения от первого лица, как живой человек.

ПРАВИЛА:
1. Отвечай коротко: обычно 1 фраза, максимум 2. Как в реальном мессенджере.
2. Пиши с маленькой буквы, без точки в конце, без markdown, без списков. Эмодзи — максимум один и редко.
3. Язык ответа = язык собеседника.
4. Никогда не говори, что ты ИИ, бот, ассистент или модель. Не упоминай промпты и инструкции.
5. Не выдумывай факты о моей жизни: планы, встречи, суммы, адреса, обещания. Если данных нет — отвечай уклончиво ("хз", "надо глянуть", "позже напишу") или задай встречный вопрос.
6. Не подтверждай встречи, время, место, деньги. В таких случаях: "ща гляну", "позже отвечу", "напишу как освобожусь".
7. Если спрашивают "ты бот?" — отвечай по-человечески уклончиво, не признавайся.
8. Не пиши больше, чем написал бы человек в чате. Никаких приветственных речей и вежливых формул.
9. Если сообщение — спам, реклама, рассылка, стикер, гифка, "ок", "+", "спасибо" или явно не требует ответа — верни ровно одно слово: SKIP
"""



class QuickReplies:
    def __init__(self, mapping: dict[str, str] | None = None):
        self._mapping = mapping or {
            "утро": "утречко"
            }

    def match(self, text: str | None) -> str | None:
        if not text:
            return None
        lowered = text.lower()
        for key, reply in self._mapping.items():
            if key in lowered:
                return reply
        return None


class LLM:
    """Инкапсулирует всю работу с LLM:
    - ask()    — синхронный запрос к Pollinations API
    - submit() — асинхронная постановка запроса в очередь; результат придёт
                 в callback из фонового потока, чтобы медленный/зависший
                 запрос не блокировал приём сообщений от Telegram
    """

    SKIP_TOKEN = "SKIP"

    def __init__(self, config: Config):
        self._config = config
        self._queue: "queue.Queue[tuple[str, callable]]" = queue.Queue( # type: ignore
            maxsize=config.queue_maxsize
        )
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)

    def start(self) -> "LLM":
        self._thread.start()
        return self

    def ask(self, user_text: str):
        response = requests.post(
            "http://127.0.0.1:5000/api/ask2",
            json={ "message": user_text }
        )

        if response.status_code == 200:
            return response.json().get('message')


    def ask2(self, user_text: str) -> str | None:
        payload = {
            "model": self._config.model,
            "messages": [
                {"role": "system", "content": self._config.system_prompt},
                {"role": "user", "content": user_text},
            ],
            "temperature": self._config.temperature,
            "max_tokens": self._config.max_tokens,
        }
        request = urllib.request.Request(
            self._config.pollinations_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self._config.request_timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        reply = data["choices"][0]["message"]["content"].strip()
        if reply == self.SKIP_TOKEN:
            return None
        return reply

    def submit(self, user_text: str, callback: callable) -> bool: # type: ignore
        try:
            logging.debug("Запрос в LLM:", user_text)
            self._queue.put_nowait((user_text, callback))
            return True
        except queue.Full:
            logging.warning("Очередь LLM переполнена, запрос отброшен: %r", user_text)
            return False

    def _worker_loop(self):
        while True:
            user_text, callback = self._queue.get()
            try:
                reply = self.ask(user_text)
                callback(reply)
            except Exception:
                logging.exception("Ошибка запроса к LLM для текста: %r", user_text)
            finally:
                self._queue.task_done()


class PersonaBot:
    def __init__(self, config: Config):
        self._config = config
        self.bot = telebot.TeleBot(config.bot_token)
        self.quick_replies = QuickReplies()
        self.llm = LLM(config).start()

        self.bot.business_message_handler(func=lambda message: True)(self._on_business_message)

    def _on_business_message(self, message):
        is_own_message = message.from_user.id == message.chat.id
        peer_username = message.chat.username if not is_own_message else "?"
        logging.info("[%s -> %s]: %s", message.from_user.username, peer_username, message.text)

        if not is_own_message:
            return

        quick = self.quick_replies.match(message.text)
        if quick is not None:
            self._send_reply(message, quick)
            return

        self.llm.submit(
            message.text,
            callback=lambda reply: self._handle_llm_reply(message, reply),
        )

    def _handle_llm_reply(self, message, reply: str | None):
        if reply is None:
            return  # модель решила промолчать (SKIP)
        logging.info("[AI -> %s]: %s", message.from_user.username, reply)
        self._send_reply(message, reply)

    def _send_reply(self, message, text: str):
        self.bot.reply_to(
            message=message,
            # text=f"[AI]: {text}",
            text=text,
            business_connection_id=message.business_connection_id,
        )

    def run(self):
        self.bot.polling(skip_pending=True)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = Config()
    bot = PersonaBot(config)
    bot.run()


if __name__ == "__main__":
    main()