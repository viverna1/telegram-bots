from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Self

from .repo_item import RepoItem


@dataclass
class User(RepoItem):
    username: str | None
    first_name: str
    registered_at: datetime

    @classmethod
    def from_dict(cls, params: dict[str, Any]) -> Self:
        data = dict(params)
        if isinstance(data.get("registered_at"), str):
            data["registered_at"] = datetime.fromisoformat(data["registered_at"])
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["registered_at"] = self.registered_at.isoformat()
        return data
