from core.domain.repository import Repository
from core.domain.user import User
from core.infrastructure.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, repo: Repository) -> None:
        super().__init__(repo, User)
