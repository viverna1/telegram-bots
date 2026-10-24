import logging

from core.domain.repo_item import RepoItem
from core.domain.repository import Repository

log = logging.getLogger(__name__)


class BaseRepository[T: RepoItem]:
    def __init__(self, repo: Repository, item_type: type[T]) -> None:
        self._repo: Repository = repo
        self._item_type: type[T] = item_type
        self._data: list[T] = []
        self._load()

    def has(self, item_id: int) -> bool:
        for item in self._data:
            if item.id == item_id:
                return True
        return False

    def add(self, item: T) -> T:
        existing = self.get(item.id)
        if existing is not None:
            return existing

        self._data.append(item)
        self._save()
        return item

    def get(self, item_id: int) -> T | None:
        for item in self._data:
            if item.id == item_id:
                return item
        return None

    def get_all(self) -> list[T]:
        return list(self._data)

    def update(self, item: T) -> T:
        for i, it in enumerate(self._data):
            if it.id == item.id:
                self._data[i] = item
                self._save()
                return item
        raise KeyError(item.id)

    def delete(self, item_id: int) -> None:
        self._data = [item for item in self._data if item.id != item_id]
        self._save()

    def _save(self) -> None:
        data = [item.to_dict() for item in self._data]
        self._repo.save(data)

    def _load(self) -> None:
        if not self._repo.exists():
            return

        data = self._repo.load()
        self._data = [self._item_type.from_dict(item) for item in data]
