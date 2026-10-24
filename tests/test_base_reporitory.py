from dataclasses import dataclass
from typing import Self

import pytest

from core.domain.repo_item import RepoItem
from core.infrastructure.base_repository import BaseRepository
from tests.fake_repository import FakeRepository


@dataclass
class Item(RepoItem):
    id: int
    name: str = ""

    @classmethod
    def from_dict(cls, params: dict) -> Self:
        return cls(id=params["id"], name=params.get("name", ""))

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}


@pytest.fixture
def fake_repo():
    return FakeRepository()


@pytest.fixture
def base_repo(fake_repo):
    return BaseRepository(fake_repo)


# ==================== Tests ====================


def test_add(base_repo):
    base_repo.add(Item(id=1))
    assert base_repo.has(1) is True


def test_add_duplicate(base_repo):
    base_repo.add(Item(id=1, name="a"))
    base_repo.add(Item(id=1, name="b"))

    assert base_repo.get_all() == [Item(id=1, name="a")]


def test_has(base_repo):
    assert base_repo.has(1) is False

    base_repo.add(Item(id=1))
    assert base_repo.has(1) is True

    assert base_repo.has(2) is False


def test_get(base_repo):
    base_repo.add(Item(id=1))
    assert base_repo.get(1) == Item(id=1)

    assert base_repo.get(2) is None


def test_get_all(base_repo):
    base_repo.add(Item(id=1))
    base_repo.add(Item(id=2))

    assert base_repo.get_all() == [Item(id=1), Item(id=2)]


def test_get_all_returns_copy(base_repo):
    base_repo.add(Item(id=1))
    result = base_repo.get_all()
    result.append(Item(id=2))
    assert len(base_repo.get_all()) == 1


def test_update(base_repo):
    base_repo.add(Item(id=1, name="a"))
    base_repo.update(Item(id=1, name="b"))
    assert base_repo.get(1) == Item(id=1, name="b")


def test_delete(base_repo):
    base_repo.add(Item(id=1))
    base_repo.add(Item(id=2))
    base_repo.delete(1)
    assert base_repo.get_all() == [Item(id=2)]
