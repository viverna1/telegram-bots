from core.domain.chat import Chat
from core.domain.repository import Repository
from core.infrastructure.base_repository import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, repo: Repository) -> None:
        super().__init__(repo, Chat)
