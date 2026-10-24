from datetime import datetime

import pytest

from core.domain.user import User


@pytest.fixture
def user_raw() -> dict:
    return {
        "id": 14,
        "username": "us",
        "first_name": "v-v",
        "registered_at": "2026-01-01T00:00:00",
    }


@pytest.fixture
def user(user_raw) -> User:
    return User.from_dict(user_raw)


def test_from_dict(user_raw):
    user = User.from_dict(user_raw)

    assert user.id == user_raw["id"]
    assert user.username == user_raw["username"]
    assert user.first_name == user_raw["first_name"]
    assert user.registered_at == datetime.fromisoformat(user_raw["registered_at"])


def test_to_dict(user, user_raw):
    assert user.to_dict() == user_raw


def test_roundtrip(user_raw):
    assert User.from_dict(user_raw).to_dict() == user_raw
