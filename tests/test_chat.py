import pytest

from core.domain.chat import Chat
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


def test_from_dict(user_raw, user):
    chat = Chat.from_dict({"id": 1, "users": [user_raw]})

    assert chat.id == 1
    assert chat.users == [user]


def test_to_dict(user, user_raw):
    chat = Chat(id=1, users=[user])

    assert chat.to_dict() == {"id": 1, "users": [user_raw]}


def test_chat_roundtrip(user_raw):
    data = {"id": 1, "users": [user_raw]}
    assert Chat.from_dict(data).to_dict() == data
