from datetime import datetime

from aiogram.types import Message

from core.domain.chat import Chat
from core.domain.user import User
from core.root import user_service


def aio_to_chat(message: Message) -> Chat:
    from_user = message.from_user
    if from_user is None:
        return Chat(id=message.chat.id, users=[])

    users: list[User] = [
        User(
            id=from_user.id,
            username=from_user.username,
            first_name=from_user.first_name,
            registered_at=datetime.now(),
        )
    ]

    if (
        message.business_connection_id is not None
        and message.chat.id != from_user.id
    ):
        owner = user_service.get_user(message.chat.id)
        if owner is not None:
            users.append(owner)

    return Chat(id=message.chat.id, users=users)