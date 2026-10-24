from datetime import datetime

import pytest

from core.application.user_service import UserService
from core.domain.user import User
from core.infrastructure.user_repository import UserRepository
from tests.fake_repository import FakeRepository


def create_user(user_id):
    return User(
        id=user_id,
        username=f"us-{user_id}",
        first_name=f"name-{user_id}",
        registered_at=datetime.now(),
    )


@pytest.fixture
def fake_repo():
    return FakeRepository()


@pytest.fixture
def user_repository(fake_repo):
    return UserRepository(fake_repo)


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)


# ==================== Tests ====================


def test_create_has_get_user(user_service: UserService):

    user1 = create_user(1)

    assert user_service.has_user(1) == False
    user_service.create_user(user1)
    assert user_service.has_user(1) == True
    assert user_service.get_user(1) == user1

    user_service.create_user(user1)
    assert user_service.get_all_users() == [user1]


def test_get_all_users(user_service: UserService):
    user1 = create_user(1)
    user2 = create_user(2)

    user_service.create_user(user1)
    user_service.create_user(user2)

    assert user_service.get_all_users() == [user1, user2]

    users = user_service.get_all_users()
    users.clear()
    assert user_service.get_all_users() == [user1, user2]


def test_update_user(user_service: UserService):

    user1 = create_user(1)
    user_service.create_user(user1)

    user1.username = "us-2"
    user_service.update_user(user1)

    final_user = user_service.get_user(1)

    assert final_user is not None
    assert final_user.username == "us-2"


def test_delete_user(user_service: UserService):
    user1 = create_user(1)
    user_service.create_user(user1)

    user_service.delete_user(1)

    assert user_service.get_all_users() == []
