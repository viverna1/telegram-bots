from dataclasses import dataclass
from enum import Enum
from typing import Any, Self

from .repo_item import RepoItem
from .user import User


class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"
    BUSINESS = "business"


@dataclass
class Chat(RepoItem):
    type: ChatType
    users: list[User] | None

    def is_private(self) -> bool:
        return self.type not in (ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL)

    def get_other_user(self, user_id: int) -> User | None:
        if not self.users:
            return None
        return next((u for u in self.users if u.id != user_id), None)

    @classmethod
    def from_dict(cls, params: dict[str, Any]) -> Self:
        data = dict(params)
        if data["users"] is not None:
            data["users"] = [User.from_dict(u) for u in data["users"]]
        data["type"] = ChatType(data["type"])
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "users": [u.to_dict() for u in self.users]
            if self.users is not None
            else None,
        }
