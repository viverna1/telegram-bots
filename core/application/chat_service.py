from core.domain.chat import Chat
from core.domain.user import User
from core.infrastructure.chat_repository import ChatRepository


class ChatService:
    def __init__(self, chat_repository: ChatRepository) -> None:
        self._chat_repository = chat_repository

    def get_chat(self, chat_id: int) -> Chat | None:
        return self._chat_repository.get(chat_id)

    def get_all_chats(self) -> list[Chat]:
        return self._chat_repository.get_all()

    def has_chat(self, chat_id: int) -> bool:
        return self._chat_repository.has(chat_id)

    def create_chat(self, chat: Chat) -> Chat:
        if self.has_chat(chat.id):
            return self.update_chat(chat)
        else:
            return self._chat_repository.add(chat)

    def upsert_chat_users(self, chat: Chat) -> Chat:
        existing_chat = self.get_chat(chat.id)
    
        if existing_chat is None:
            return self.create_chat(chat)
    
        for user in chat.users:
            self.add_member(existing_chat, user, save=False)
    
        self._chat_repository._save()
        return existing_chat
    
    def add_member(self, chat: Chat, new_member: User, save: bool = True) -> Chat:
        existing_ids = {u.id for u in chat.users}
        if new_member.id not in existing_ids:
            chat.users.append(new_member)
    
        if save:
            self._chat_repository._save()
        return chat
        

    def update_chat(self, chat: Chat) -> Chat:
        return self._chat_repository.update(chat)

    def delete_chat(self, chat_id: int) -> None:
        self._chat_repository.delete(chat_id)
