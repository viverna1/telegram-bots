from pathlib import Path

from core.application.chat_service import ChatService
from core.application.user_service import UserService
from core.infrastructure.chat_repository import ChatRepository
from core.infrastructure.json_repository import JsonRepository
from core.infrastructure.user_repository import UserRepository

_DATA = Path(__file__).resolve().parent.parent / "data"

_json_repository = JsonRepository(str(_DATA / "users.json"))
_user_repository = UserRepository(_json_repository)
user_service = UserService(_user_repository)

_json_repository = JsonRepository(str(_DATA / "chats.json"))
_chat_repository = ChatRepository(_json_repository)
chat_service = ChatService(_chat_repository)
