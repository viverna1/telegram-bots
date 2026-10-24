from dataclasses import dataclass
from typing import Any, Self

from .repo_item import RepoItem
from .user import User


@dataclass
class Chat(RepoItem):
    users: list[User]

    @classmethod
    def from_dict(cls, params: dict[str, Any]) -> Self:
        data = dict(params)
        data["users"] = [User.from_dict(u) for u in data["users"]]
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "users": [u.to_dict() for u in self.users],
        }
