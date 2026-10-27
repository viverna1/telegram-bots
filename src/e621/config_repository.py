import json
import logging
from typing import Any

log = logging.getLogger(__name__)


class ConfigRepository:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self._data: dict[str, Any] = self.load()

    def get_tags(self) -> str:
        return self._data.get("tags", "")

    def get_sent_posts_id(self) -> list[int]:
        return self._data.get("sent-posts", [])

    def get_headers(self) -> dict[str, str]:
        return self._data.get("headers", {})

    def get_limit(self) -> int:
        return self._data.get("limit", 10)

    def mark_post_as_sent(self, post_id: int) -> None:
        if post_id not in self.get_sent_posts_id():
            self._data["sent-posts"].append(post_id)
            self.save()

    def load(self) -> dict[str, Any]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)