import json
import logging
import os

from core.domain.repository import Repository

log = logging.getLogger(__name__)


class JsonRepository(Repository):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def exists(self) -> bool:
        return os.path.exists(self.filepath)

    def load(self) -> list:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            log.exception("Ошибка загрузки: %s", self.filepath)
            raise

    def save(self, data: list) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
