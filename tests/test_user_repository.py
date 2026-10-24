from datetime import datetime

import pytest
from pytest_mock import MockerFixture

from core.domain.user import User
from core.infrastructure.user_repository import UserRepository


def create_user(user_id):
    return User(
        id=user_id,
        username=f"us-{user_id}",
        first_name=f"name-{user_id}",
        registered_at=datetime.now(),
    )


@pytest.fixture
def mock_user_repository(mocker: MockerFixture):
    mock_load = mocker.patch.object(UserRepository, "_load")
    mock_save = mocker.patch.object(UserRepository, "_save")
    return mock_load, mock_save


@pytest.fixture
def user_repository(tmp_path, mock_user_repository):
    return UserRepository(str(tmp_path / "users.json"))


# ==================== Tests ====================


def test_add_has_get_user(user_repository: UserRepository, mock_user_repository):
    _, mock_save = mock_user_repository

    user1 = create_user(1)

    assert user_repository.has_user(1) == False
    user_repository.add_user(user1)
    assert user_repository.has_user(1) == True
    assert user_repository.get_user(1) == user1

    user_repository.add_user(user1)
    assert user_repository.get_all_users() == [user1]
    
    assert mock_save.call_count == 1


def test_roundtrip(tmp_path):
    path = str(tmp_path / "users.json")
    repo = UserRepository(path)
    user = create_user(1)
    repo.add_user(user)

    repo2 = UserRepository(path)
    assert repo2.get_user(1) == user


def test_get_all_users(user_repository: UserRepository):
    user1 = create_user(1)
    user2 = create_user(2)
    
    user_repository.add_user(user1)
    user_repository.add_user(user2)

    assert user_repository.get_all_users() == [user1, user2]

    users = user_repository.get_all_users()
    users.clear()
    assert user_repository.get_all_users() == [user1, user2]


def test_update_user(user_repository: UserRepository, mock_user_repository):
    _, mock_save = mock_user_repository

    user1 = create_user(1)
    user_repository.add_user(user1)

    user1.username = "us-2"
    user_repository.update_user(user1)

    final_user = user_repository.get_user(1)

    assert final_user is not None
    assert final_user.username == "us-2"

    assert mock_save.call_count == 2


def test_delete_user(user_repository: UserRepository, mock_user_repository):
    _, mock_save = mock_user_repository

    user1 = create_user(1)
    user_repository.add_user(user1)

    user_repository.delete_user(1)

    assert user_repository.get_all_users() == []
    
    assert mock_save.call_count == 2
