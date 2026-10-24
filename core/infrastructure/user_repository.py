import json
import os

from core.domain.user import User


class UserRepository:
    def __init__(self, save_file: str):
        self._users: list[User] = []
        self._save_file = save_file
        self._load()

    def has_user(self, user_id: int) -> bool:
        for user in self._users:
            if user.id == user_id:
                return True
        return False

    def add_user(self, user: User) -> User:
        if self.has_user(user.id):
            return user

        self._users.append(user)
        self._save()
        return user

    def get_user(self, user_id: int) -> User | None:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def get_all_users(self) -> list[User]:
        return list(self._users)

    def update_user(self, user: User) -> User | None:
        for i, u in enumerate(self._users):
            if u.id == user.id:
                self._users[i] = user
                self._save()
                return u

    def delete_user(self, user_id: int) -> None:
        self._users = [u for u in self._users if u.id != user_id]
        self._save()

    def _save(self) -> None:
        data = [user.to_dict() for user in self._users]
        with open(self._save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load(self) -> None:
        if not os.path.exists(self._save_file):
            return

        with open(self._save_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._users = [User.from_dict(user) for user in data]
