from core.domain.user import User
from core.infrastructure.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> User | None:
        return self.user_repository.get_user(user_id)

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def has_user(self, user_id: int) -> bool:
        return self.user_repository.has_user(user_id)

    def create_user(self, user: User) -> User:
        if self.has_user(user.id):
            return self.update_user(user)
        else:
            return self.user_repository.add_user(user)

    def update_user(self, user: User) -> User | None:
        return self.user_repository.update_user(user)

    def delete_user(self, user_id: int) -> None:
        self.user_repository.delete_user(user_id)
