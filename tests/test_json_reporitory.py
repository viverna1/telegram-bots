import json

import pytest

from core.infrastructure.json_repository import JsonRepository


@pytest.fixture
def repo_path(tmp_path):
    return tmp_path / "users.json"


@pytest.fixture
def repo(repo_path):
    return JsonRepository(str(repo_path))


# ==================== Tests ====================


def test_constructor_stores_filepath(tmp_path):
    path = str(tmp_path / "x.json")
    assert JsonRepository(path).filepath == path


def test_exists_false_when_file_missing(repo):
    assert repo.exists() is False


def test_exists_true_when_file_present(repo, repo_path):
    repo_path.write_text("[]", encoding="utf-8")
    assert repo.exists() is True


def test_save_writes_valid_json(repo, repo_path):
    data = [{"id": 1}, {"id": 2}]
    repo.save(data)
    assert json.loads(repo_path.read_text(encoding="utf-8")) == data


def test_save_overwrites_existing(repo, repo_path):
    repo.save([{"id": 1}])
    repo.save([{"id": 2}])
    assert json.loads(repo_path.read_text(encoding="utf-8")) == [{"id": 2}]


def test_load_returns_data(repo, repo_path):
    repo_path.write_text(json.dumps([{"id": 1}]), encoding="utf-8")
    assert repo.load() == [{"id": 1}]


def test_roundtrip(repo_path):
    data = [{"id": 1}, {"id": 2}]
    JsonRepository(str(repo_path)).save(data)
    assert JsonRepository(str(repo_path)).load() == data
