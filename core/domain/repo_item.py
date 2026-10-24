from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Self


@dataclass
class RepoItem(ABC):
    id: int

    @classmethod
    @abstractmethod
    def from_dict(cls, params: dict) -> Self:
        data = dict(params)
        return cls(**data)


    def to_dict(self) -> dict:
        return asdict(self)
