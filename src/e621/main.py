import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
STATE_FILE = "e621_state.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_post_id": 0}


def save_state(last_id):
    with open(STATE_FILE, "w") as f:
        state = {"last_post_id": last_id, "last_update": datetime.now().isoformat()}
        json.dump(state, f, indent=2)


def get_new_posts(limit=10):
    # Загружаем последний известный ID
    state = load_state()
    last_id = state.get("last_post_id", 0)

    url = "https://e621.net/posts.json"

    params = {
        "limit": limit,
        "order": "id",  # Сортировка от старых к новым
    }

    # Если есть последний ID, ищем только посты новее его
    if last_id > 0:
        params["tags"] = f"id:>{last_id}"
    else:
        print("Первый запуск - загружаем последние посты")

    headers = {"User-Agent": "e621TelegramBot/1.0 (by Covi)"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()
    posts = data.get("posts", [])

    # Находим максимальный ID среди новых постов
    if posts:
        max_id = max(post.get("id", 0) for post in posts)
        save_state(max_id)

        print("Последний Id:", max_id)
    else:
        pass

    return posts


if __name__ == "__main__":
    new_posts = get_new_posts(limit=10)

    if new_posts:
        print(f"\nНовые посты ({len(new_posts)} шт.):")
        for i, post in enumerate(new_posts, 1):
            print(f"{i}. ID: {post.get('id')}")

    else:
        print("Новых постов нет.")
