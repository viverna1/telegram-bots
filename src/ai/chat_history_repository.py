from dataclasses import dataclass, field

from core.domain.repo_item import RepoItem
from core.domain.repository import Repository
from core.infrastructure.base_repository import BaseRepository


@dataclass
class ChatHistory(RepoItem):
    history: list[dict[str, str]] = field(default_factory=list)


class ChatHistoryRepository(BaseRepository[ChatHistory]):
    def __init__(self, repo: Repository) -> None:
        super().__init__(repo, ChatHistory)

    def get_chat_history(self, chat_id: int) -> list[dict[str, str]] | None:
        chat = self.get(chat_id)
        if chat is None:
            return None
        return chat.history

    def add_message(self, chat_id: int, message: dict[str, str]) -> None:
        chat = self.get(chat_id)
        if chat is None:
            chat = self.add(ChatHistory(chat_id))

        chat.history.append(message)
        if len(chat.history) > 10:
            chat.history.pop(0)

        self.update(chat)
