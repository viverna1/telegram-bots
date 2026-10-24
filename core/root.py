from pathlib import Path

from core.application.user_service import UserService
from core.infrastructure.user_repository import UserRepository

_DATA = Path(__file__).resolve().parent.parent / "data" / "users.json"

_user_repository = UserRepository(str(_DATA))
user_service = UserService(_user_repository)
