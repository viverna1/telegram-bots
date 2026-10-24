from datetime import datetime

from aiogram.types import Message

from core.domain.chat import Chat, ChatType
from core.domain.user import User
from core.root import user_service


def aio_to_chat(message: Message) -> Chat:
    from_user = message.from_user
    chat_type = get_chat_type(message)

    if chat_type in (ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL):
        return Chat(id=message.chat.id, type=ChatType(chat_type), users=None)

    if from_user is None:
        return Chat(id=message.chat.id, type=ChatType(chat_type), users=[])


    users: list[User] | None = None
    
    if chat_type == ChatType.BUSINESS:
        user = user_service.get_user(from_user.id)
        if user is None:
            user = User(
                id=from_user.id,
                username=from_user.username,
                first_name=from_user.first_name,
                registered_at=datetime.now(),
            )
            
        users = [user]
        
        if message.chat.id != from_user.id:
            owner = user_service.get_user(message.chat.id)
            if owner is not None:
                users.append(owner)

    elif chat_type == ChatType.PRIVATE:
        users = None

    return Chat(id=message.chat.id, type=ChatType(chat_type), users=users)


def get_chat_type(message: Message) -> ChatType:
    if message.business_connection_id is not None:
        return ChatType.BUSINESS
    else:
        return ChatType(message.chat.type)