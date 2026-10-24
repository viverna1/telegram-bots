from core.domain.chat import Chat
from core.domain.user import User
from core.infrastructure.chat_repository import ChatRepository


class ChatService:
    def __init__(self, chat_repository: ChatRepository) -> None:
        self._repo = chat_repository

    def get_chat(self, chat_id: int) -> Chat | None:
        return self._repo.get(chat_id)

    def get_all_chats(self) -> list[Chat]:
        return self._repo.get_all()

    def has_chat(self, chat_id: int) -> bool:
        return self._repo.has(chat_id)

    def create_chat(self, chat: Chat) -> Chat:
        if self.has_chat(chat.id):
            return self.update_chat(chat)
        else:
            return self._repo.add(chat)

    def upsert_chat_users(self, chat: Chat) -> None:
        existing_chat = self.get_chat(chat.id)
        if existing_chat is None:
            self.create_chat(chat)
            return
            
        if not existing_chat.is_private() or chat.users is None:
            return


        for user in chat.users:
            self.add_member(existing_chat, user)

        self._repo.update(existing_chat)

    def add_member(self, chat: Chat, new_member: User) -> None:
        if chat.users is None:
            return
        existing_ids = {u.id for u in chat.users}
        if new_member.id not in existing_ids:
            chat.users.append(new_member)

    def update_chat(self, chat: Chat) -> Chat:
        return self._repo.update(chat)

    def delete_chat(self, chat_id: int) -> None:
        self._repo.delete(chat_id)
