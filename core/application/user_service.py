from core.domain.user import User
from core.infrastructure.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def get_user(self, user_id: int) -> User | None:
        return self._user_repository.get(user_id)

    def get_all_users(self) -> list[User]:
        return self._user_repository.get_all()

    def has_user(self, user_id: int) -> bool:
        return self._user_repository.has(user_id)

    def create_user(self, user: User) -> User:
        if self.has_user(user.id):
            return self.update_user(user)
        else:
            return self._user_repository.add(user)

    def update_user(self, user: User) -> User:
        return self._user_repository.update(user)

    def delete_user(self, user_id: int) -> None:
        self._user_repository.delete(user_id)
